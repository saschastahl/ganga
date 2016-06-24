##########################################################################
# Ganga Project. http://cern.ch/ganga
#
# $Id: Objects.py,v 1.5.2.10 2009-07-24 13:35:53 ebke Exp $
##########################################################################
# NOTE: Make sure that _data and __dict__ of any GangaObject are only referenced
# here - this is necessary for write locking and lazy loading!
# IN THIS FILE:
# * Make sure every time _data or __dict__ is accessed that _data is not None. If yes, do:
#    obj._getReadAccess()
# * Make sure every write access is preceded with:
#    obj._getWriteAccess()
#   and followed by
#    obj._setDirty()

import abc
import threading
from contextlib import contextmanager
import functools

from Ganga.Utility.logging import getLogger

from copy import deepcopy, copy
from inspect import isclass

from Ganga.GPIDev.Schema import Schema, Item, ComponentItem, SharedItem

from Ganga.Core.exceptions import GangaValueError, GangaException

from Ganga.Utility.Plugin import allPlugins

def _getName(obj):
    """ Return the name of an object based on what we prioritise 
    Name is defined as the first in the list of:
    obj._name, obj.__name__, obj.__class__.__name__ or str(obj)
    Args:
        obj (unknown):
    """
    returnable = getattr(obj, '_name', getattr(obj, '__name__', None))
    if returnable is None:
        returnable = getattr(getattr(obj, '__class__', None), '__name__', None)
    if returnable is None:
        returnable = str(obj)
    return returnable

logger = getLogger(modulename=1)

_imported_GangaList = None

do_not_copy = ['_index_cache_dict', '_parent', '_registry', '_data', '_read_lock', '_write_lock', '_proxyObject']

def _getGangaList():
    """
    This method gets around the problem that GangaList can't be imported at a module level here
    """
    global _imported_GangaList
    if _imported_GangaList is None:
        from Ganga.GPIDev.Lib.GangaList.GangaList import GangaList
        _imported_GangaList = GangaList
    return _imported_GangaList


def synchronised(f):
    """
    This decorator must be attached to a method on a ``Node`` subclass
    It uses the object's lock to make sure that the object is held for the duration of the decorated function
    Args:
        f (function): This is the function which we want to wrap
    """
    @functools.wraps(f)
    def decorated(self, *args, **kwargs):
        with self.const_lock:
            return f(self, *args, **kwargs)
    return decorated


class Node(object):
    """
    The Node class is the code of the Ganga heirachy. It allows objects to keep
    track of their parent, whether they're dirty and take part in the visitor
    pattern.

    It also provides access to tree-aware read/write locks to provide
    thread-safe usage.
    """
    __metaclass__ = abc.ABCMeta
    __slots__ = ('_parent', '_read_lock', '_write_lock', '_dirty')

    def __init__(self, parent=None):
        super(Node, self).__init__()
        self._parent = parent
        self._read_lock = threading.RLock()  # Don't read out of thread whilst we're making a change
        self._write_lock = threading.RLock()  # Don't write from out of thread when modifying an object
        self._dirty = False  # dirty flag is true if the object has been modified locally and its contents is out-of-sync with its repository

    def __deepcopy__(self, memo=None):
        cls = self.__class__
        obj = cls()
        for elem, obj in self.__dict__.iteritems():
            if elem not in do_not_copy:
                setattr(obj, elem, deepcopy(obj, memo))

        parent_ = self._getParent()
        if parent_ is not None:
            obj._setParent(parent_)
        return obj

    def _getParent(self):
        """
        This gets the parent object defined for this Node
        """
        # type: () -> Node
        return self._parent

    @synchronised  # This will lock the _current_ (soon to be _old_) root object
    def _setParent(self, parent):
        """
        This sets the parent of this Node to be a new object
        Args:
            parent (GangaObject): This is the GangaObject to be taken as the objects new parent
        """
        # type: (Node) -> None
        if parent is None:
            setattr(self, '_parent', parent)
        else:
            with parent.const_lock: # This will lock the _new_ root object
                setattr(self, '_parent', parent)
            # Finally the new and then old root objects will be unlocked

    @property
    @contextmanager
    def const_lock(self):
        """
        This is a context manager which acquires the const write lock on the
        object's root object.

        This lock acquires exclusive access over an object tree to prevent it
        changing. Reading schema attributes on the object is still allowed
        but changing them is not. Only one thread can hold this lock at once.
        """
        root = self._getRoot()
        reg = root._getRegistry()
        root._read_lock.acquire()
        root._write_lock.acquire()
        try:
            yield
        finally:
            root._write_lock.release()
            root._read_lock.release()

    def _getRoot(self, cond=None):
        # type: () -> Node
        """
        get the root of the object tree
        if parent does not exist then the root is the 'self' object
        cond is an optional function which may cut the search path: when it
        returns True, then the parent is returned as root
        """
        if self._getParent() is None:
            return self
        root = None
        obj = self
        cond_test = cond is not None
        while obj is not None:
            root = obj
            if cond_test:
                if cond(root):
                    break
            obj = obj._getParent()
        return root

    # accept a visitor pattern
    @abc.abstractmethod
    def accept(self, visitor):
        """
        This can probably be removed if it doesn't do anything, only GangaObjet should inherit from Node
        """
        pass

    # mark object as "dirty" and inform the registry about it
    # the registry is always associated with the root object
    def _setDirty(self):
        """ Set the dirty flag all the way up to the parent"""
        self._dirty = True
        parent = self._getParent()
        if parent is not None:
            parent._setDirty()

    def _setFlushed(self):
        """
        This returns whether this object has been marked as dirty or not
        """
        self._dirty = False

    def printTree(self, f=None, sel=''):
        """
        This method will print a full tree which contains a full description of the class which of interest
        Args:
            f (stream): file-like output stream
            sel (str): Selection to display 
        """
        from Ganga.GPIDev.Base.VPrinter import VPrinter
        self.accept(VPrinter(f, sel))

    def printSummaryTree(self, level=0, verbosity_level=0, whitespace_marker='', out=None, selection='', interactive=False):
        """If this method is overridden, the following should be noted:

        Args:
            level (int): the hierachy level we are currently at in the object tree.
            verbosity_level (int): How verbose the print should be. Currently this is always 0.
            whitespace_marker (str): If printing on multiple lines, this allows the default indentation to be replicated.
                               The first line should never use this, as the substitution is 'name = %s' % printSummaryTree()
            out (stream): An output stream to print to. The last line of output should be printed without a newline.'
            selection (str): See VPrinter for an explaintion of this.
            interactive (bool): Is this being printed to the interactive prompt
        """
        from Ganga.GPIDev.Base.VPrinter import VSummaryPrinter
        self.accept(VSummaryPrinter(level, verbosity_level, whitespace_marker, out, selection, interactive))

    @abc.abstractmethod
    def __eq__(self, node):
        """
        This can probably be removed if it doesn't do anything, only GangaObjet should inherit from Node
        """
        pass

    def __ne__(self, node):
        """
        This can probably be removed if it doesn't do anything, only GangaObjet should inherit from Node
        """
        return not self.__eq__(node)

##########################################################################


def synchronised_get_descriptor(get_function):
    """
    This decorator should only be used on ``__get__`` method of the ``Descriptor``.
    Args:
        get_function (function): Function we intend to wrap with the soft/read lock
    """
    @functools.wraps(get_function)
    def decorated(self, obj, type_or_value):
        if obj is None:
            return get_function(self, obj, type_or_value)

        with obj._read_lock:
            return get_function(self, obj, type_or_value)

    return decorated


def synchronised_set_descriptor(set_function):
    """
    This decorator should only be used on ``__set__`` method of the ``Descriptor``.
    Args:
        set_function (function): Function we intend to wrap with the hard/write lock
    """
    def decorated(self, obj, type_or_value):
        if obj is None:
            return set_function(self, obj, type_or_value)

        with obj._read_lock:
            with obj.const_lock:
                return set_function(self, obj, type_or_value)
    return decorated


class Descriptor(object):

    """
    This is the Descriptor class used to deal with object assignment ot attribtues of the GangaObject.
    This class handles the lazy-loading of an object from disk when needed to resturn a value stored in the Registry
    This class also handles thread-locking of a class including both the getter and setter methods to ensure object consistency
    """

    def __init__(self, name, item):
        """
        Lets build a descriptor for this item with this name
        Args:
            name (str): Name of the attribute being wrapped
            item (Item): The Schema entry describing this attribute (Not currently used atm)
        """
        self._name = name
        self._item = item
        self._checkset_name = None
        self._filter_name = None

        self._getter_name = item['getter']
        self._checkset_name = item['checkset']
        self._filter_name = item['filter']

    @staticmethod
    def _bind_method(obj, name):
        """
        Method which returns the value for a given attribute of a name
        Args:
            name (str): This is the name of the attribute of interest
        """
        if name is None:
            return None
        return getattr(obj, name)

    def _check_getter(self):
        """
        This attribute checks to see if a getter has been assigned to an attribute or not to avoid it's assignment
        """
        if self._getter_name:
            raise AttributeError('cannot modify or delete "%s" property (declared as "getter")' % _getName(self))

    @synchronised_get_descriptor
    def __get__(self, obj, cls):
        """
        Get method of Descriptor
        This wraps the object in question with a read-lock which ensures object onsistency across multiple threads
        Args:
            obj (GangaObject): This is the object which controls the attribute of interest
            cls (class): This is the class of the Ganga Object which is being called
        """
        name = _getName(self)

        # If obj is None then the getter was called on the class so return the Item
        if obj is None:
            return cls._schema[name]

        # If this class has an associated getter method make use of that
        if self._getter_name:
            return self._bind_method(obj, self._getter_name)()

        # First we want to try to get the information without prompting a load from disk

        # If we're laded from disk inspect the _data and generate a default if needed
        # If we're not loaded from disk, we should _by definition_ NOT look here for objects in memory as they should NEVER be here
        if obj._fullyLoadedFromDisk():
            # schema data takes priority ALWAYS over ._index_cache
            # This access should not cause the object to be loaded
            if name not in obj._data:
                self.__set__(obj, obj._schema.getDefaultValue(name))
            # NB we check for schema entries as this will have problem when object not in Schema
            return obj._data[name]

        # Then try to get it from the index cache
        # NB Can we remove this yet? This allows access to index items asif they're in the schema. They are normally not.
        obj_index = obj._index_cache
        if name in obj_index:
            return obj_index[name]

        # Since we couldn't find the information in the cache, we will need to fully load the object

        # Guarantee that the object is now loaded from disk
        reg = obj._getRegistry()
        if reg:
            reg._load([obj._id])

        # If we've loaded from disk then the data dict has changed. If we're constructing an object
        # then we need to rely on the factory
        if name not in obj._data:
            self.__set__(obj, obj._schema.getDefaultValue(name))
        return obj._data[name]

        if obj._fullyLoadedFromDisk():
            # If we loaded from disk everything could have changed (including corrupt index updated!)
            obj_index = obj._index_cache
            if name in obj_index:
                return obj_index[name]

                
            # NB DO NOT, EVER explicitly rely on the full string representation of the class here as you could 
            # very easily end up in a circular loop here back at the getter for an attribute not correctly setup
            # _Try_ at least to just get the object name. The _getName method will result in performing a full string rep
            # but this method will only do that if it ABSOLUTELY NEEDS TO
            raise AttributeError('Could not find attribute "{0}" in "{1}"'.format(name, _getName(obj)))
        else:
            # GangaException as something has really gone wrong here (repo error or worse!)
            raise GangaException('Failed to load object from disk to get attribute "%s" of class: "%s"' % (name, _getName(obj)))

    @staticmethod
    def cloneObject(v, input_tuple):
        """
        Clone v using knowledge of the obj the attr is being set on and the name of self is the attribute name
        return a new instance of v equal to v
        Args:
            v (unknown): This is the object we want to clone
            obj (GangaObject): This is the parent object of the attribute
            name (str): This is the name of the attribute we want to assign the value of v to
        """
        obj = input_tuple[1]
        name = input_tuple[0]
        item = obj._schema[name]

        if v is None:
            if item.hasProperty('category'):
                assertion = item['optional'] and (item['category'] != 'internal')
            else:
                assertion = item['optional']
            #assert(assertion)
            if assertion is False:
                name = input_tuple[0]
                logger.warning("Item: '%s'. of class type: '%s'. Has a Default value of 'None' but is NOT optional!!!" % (name, type(obj)))
                logger.warning("Please contact the developers and make sure this is updated!")
            return None
        elif isinstance(v, str):
            return str(v)
        elif isinstance(v, int):
            return int(v)
        elif isinstance(v, dict):
            new_dict = {}
            for key, item in new_dict.iteritems():
                new_dict[key] = Descriptor.cloneObject(v, input_tuple)
            return new_dict
        else:
            if not isinstance(v, Node) and isinstance(v, (list, tuple)):
                try:
                    GangaList = _getGangaList()
                    new_v = GangaList()
                except ImportError:
                    new_v = []
                for elem in v:
                    new_v.append(Descriptor.cloneObject(elem, input_tuple))
                #return new_v
            elif not isinstance(v, Node):
                if isclass(v):
                    new_v = v()
                else:
                    new_v = v
                if not isinstance(new_v, Node):
                    logger.error("v: %s" % v)
                    raise GangaException("Error: found Object: %s of type: %s expected an object inheriting from Node!" % (v, type(v)))
                else:
                    new_v = Descriptor.cloneNodeObject(v, input_tuple)
            else:
                new_v = Descriptor.cloneNodeObject(v, input_tuple)

            return new_v

    @staticmethod
    def cloneNodeObject(v, input_tuple):
        """This copies objects inherited from Node class
        This is a call to deepcopy after testing to see if the object can be copied to the attribute
        Args:
            v (GangaObject): This is the value which we want to copy from
            obj (GangaObject): This is the object which controls the attribute we want to assign
            name (str): This is th name of the attribute which we're setting
        """
        obj = input_tuple[1]
        name = input_tuple[0]

        item = obj._schema[name]
        GangaList = _getGangaList()
        if isinstance(v, GangaList):
            categories = v.getCategory()
            len_cat = len(categories)
            if (len_cat > 1) or ((len_cat == 1) and (categories[0] != item['category'])) and item['category'] != 'internal':
                # we pass on empty lists, as the catagory is yet to be defined
                from Ganga.GPIDev.Base.Proxy import GangaAttributeError
                raise GangaAttributeError('%s: attempt to assign a list containing incompatible objects %s to the property in category "%s"' % (name, v, item['category']))
        else:
            if v._category not in [item['category'], 'internal'] and item['category'] != 'internal':
                from Ganga.GPIDev.Base.Proxy import GangaAttributeError
                raise GangaAttributeError('%s: attempt to assign an incompatible object %s to the property in category "%s found cat: %s"' % (name, v, item['category'], v._category))

        v_copy = deepcopy(v)

        return v_copy

    @synchronised_set_descriptor
    def __set__(self, obj, val):
        """
        Set method
        This wraps the given object with a lock preventing both read+write until this transaction is complete for consistency
        Args:
            self: attribute being changed or Ganga.GPIDev.Base.Objects.Descriptor in which case _getName(self) gives the name of the attribute being changed
            obj (GanagObject): parent class which 'owns' the attribute
            val (unknown): value of the attribute which we're about to set
        """

        if isinstance(val, str):
            from Ganga.GPIDev.Base.Proxy import stripProxy, runtimeEvalString
            val = stripProxy(runtimeEvalString(obj, _getName(self), val))

        if hasattr(obj, '_checkset_name'):
            checkSet = self._bind_method(obj, self._checkset_name)
            if checkSet is not None:
                checkSet(_val)
        if hasattr(obj, '_filter_name'):
            this_filter = self._bind_method(obj, self._filter_name)
            if this_filter:
                val = this_filter(_val)

        self._check_getter()

        # ON-DISK LOCKING
        if not obj._fullyLoadedFromDisk():
            obj._getWriteAccess()

        _set_name = _getName(self)

        # This returns a reference or new object as appropriate
        new_value = Descriptor.cleanValue(obj, val, _set_name)

        # This sets the object and assigns the parent correctly
        obj.setSchemaAttribute(_set_name, new_value)
        obj._setDirty()


    @staticmethod
    def cleanValue(obj, val, name):
        """
        This returns a new instance of the value which has been correctly copied if needed so we can assign it to the attribute of the class
        Args:
            obj (GangaObject): This is the parent object of the attribute which is being set
            val (unknown): This is the value we want to assign to the attribute
            name (str): This is the name of the attribute which we're changing
        """
        from Ganga.GPIDev.Lib.GangaList.GangaList import makeGangaList

        item = obj._schema[name]

        ## If the item has been defined as a sequence great, let's continue!
        if item['sequence']:
            # These objects are lists
            _preparable = True if item['preparable'] else False
            if len(val) == 0:
                GangaList = _getGangaList()
                new_val = GangaList()
            else:
                if isinstance(item, ComponentItem):
                    new_val = makeGangaList(val, Descriptor.cloneListOrObject, parent=obj, preparable=_preparable, extra_args=(name, obj))
                else:
                    new_val = makeGangaList(val, parent=obj, preparable=_preparable)
        else:
            ## Else we need to work out what we've got.
            if isinstance(item, ComponentItem):
                GangaList = _getGangaList()
                if isinstance(val, (list, tuple, GangaList)):
                    ## Can't have a GangaList inside a GangaList easily so lets not
                    if isinstance(obj, GangaList):
                        new_val = []
                    else:
                        new_val = GangaList()
                    # Still don't know if val list of object here
                    Descriptor.createNewList(new_val, val, Descriptor.cloneListOrObject, extra_args=(name, obj))
                else:
                    # Still don't know if val list of object here
                    new_val = Descriptor.cloneListOrObject(val, (name, obj))
            else:
                new_val = val
                pass

        if isinstance(new_val, Node):
            new_val._setParent(obj)

        return new_val

    @staticmethod
    def cloneListOrObject(v, extra_args):
        """
        This clones the value v by determining if the value of v is a list or not.
        If v is a list then a new list is returned with elements copied via cloneObject
        if v is not a list then a new instance of the list is copied via cloneObject
        Args:
            v (unknown): Object we want a new copy of
            extra_args (tuple): Contains the name of the attribute being copied and the object which owns the object being copied
        """
        GangaList = _getGangaList()
        if isinstance(v, (list, tuple, GangaList)):
            return makeGangaList(v, Descriptor.cloneObject, parent=obj, extra_args=extra_args)
        else:
            return Descriptor.cloneObject(v, extra_args)

    @staticmethod
    def createNewList(_final_list, _input_elements, action=None, extra_args=None):
        """ Create a new list object which contains the old object with a possible action parsing the elements before they're added
        Args:
            _final_list (list): The list object which is to have the new elements appended to it
            _input_elements (list): This is a list of the objects which are to be used to create new objects in _final_list
            action (function): A function which is to be called to create new objects for a list
            extra_args (tuple): Contains the name of the attribute being copied and the object which owns the object being copied
        """

        if extra_args:
            new_action = partial(action, extra_args=extra_args)

        if action is not None:
            for element in _input_elements:
                if extra_args:
                    _final_list.append(new_action(element))
                else:
                    _final_list.append(action(element))
        else:
            for element in _input_elements:
                _final_list.append(element)


class ObjectMetaclass(abc.ABCMeta):
    """
    This is a MetaClass...
    TODO explain what this does"""

    def __init__(cls, name, bases, this_dict):
        """
        Init method for a class of name, name
        TODO, explain what bases and this_dict are used for
        """

        super(ObjectMetaclass, cls).__init__(name, bases, this_dict)

        # all Ganga classes must have (even empty) schema
        if cls._schema is None:
            cls._schema = Schema(None, None)

        this_schema = cls._schema

        # Add all class members of type `Schema.Item` to the _schema object
        # TODO: We _could_ add base class's Items here by going through `bases` as well.
        # We can't just yet because at this point the base class' Item has been overwritten with a Descriptor
        for member_name, member in this_dict.items():
            if isinstance(member, Item):
                this_schema.datadict[member_name] = member

        # sanity checks for schema...
        if '_schema' not in this_dict:
            s = "Class %s must _schema (it cannot be silently inherited)" % (name,)
            logger.error(s)
            raise ValueError(s)

        attrs_to_add = tuple(attr for attr, item in this_schema.allItems())

        # This reduces the memory footprint
        # TODO explore migrating the _data object to a non-dictionary type as it's a fixed size and we can potentially save big here!
        # Adding the __dict__ here is an acknowledgement that we don't control all Ganga classes higher up.
        cls.__slots__ = ('_index_cache_dict', '_registry', '_data', '__dict__', '_proxyObject', '_inMemory') + attrs_to_add

        # If a class has not specified a '_name' then default to using the class '__name__'
        if not cls.__dict__.get('_name'):
            cls._name = name

        if this_schema._pluginclass is not None:
            logger.warning('Possible schema clash in class %s between %s and %s', name, _getName(cls), _getName(this_schema._pluginclass))

        # export visible properties... do not export hidden properties
        # This constructs one Descriptor for each attribute which can be set for this class
        for attr, item in this_schema.allItems():
            setattr(cls, attr, Descriptor(attr, item))

        # additional check of type
        # bugfix #40220: Ensure that default values satisfy the declared types
        # in the schema
        for attr, item in this_schema.simpleItems():
            if not item['getter']:
                item._check_type(item['defvalue'], '.'.join([name, attr]), enableGangaList=False)

        # create reference in schema to the pluginclass
        this_schema._pluginclass = cls

        # if we've not even declared this we don't want to use it!
        if not cls._declared_property('hidden') or cls._declared_property('enable_plugin'):
            allPlugins.add(cls, cls._category, _getName(cls))

        # create a configuration unit for default values of object properties
        if not cls._declared_property('hidden') or cls._declared_property('enable_config'):
            this_schema.createDefaultConfig()


class GangaObject(Node):
    __metaclass__ = ObjectMetaclass # Change standard Python metaclass object
    _schema = None  # obligatory, specified in the derived classes
    _category = None  # obligatory, specified in the derived classes
    _exportmethods = []  # optional, specified in the derived classes

    # by default classes are not hidden, config generation and plugin
    # registration is enabled
    # optional, specify in the class if you do not want to export it publicly
    # in GPI,
    _hidden = 1
    # the class will not be registered as a plugin unless _enable_plugin is defined
    # the test if the class is hidden is performed by x._declared_property('hidden')
    # which makes sure that _hidden must be *explicitly* declared, not
    # inherited

    # additional properties that may be set in derived classes which were declared as _hidden:
    #   _enable_plugin = 1 -> allow registration of _hidden classes in the allPlugins dictionary
    # _enable_config = 1 -> allow generation of [default_X] configuration
    # section with schema properties

    # must be fully initialized
    def __init__(self):
        """
        Main GangaObject that many classes inherit from
        """
        super(GangaObject, self).__init__(None)

        self._index_cache_dict = {}
        self._registry = None

        self._data = {}

        self._inMemory = True

    def __construct__(self, args):
        # type: (Sequence) -> None
        """
        This acts like a secondary constructor for proxy objects.
        Any positional (non-keyword) arguments are passed to this function to construct the object.

        This default implementation performs a copy if there was only one item in the list
        and raises an exception if there is more than one.

        Args:
            args: a list of objects

        Raises:
            TypeMismatchError: if there is more than one item in the list
        """
        # FIXME: This should probably be move to Proxy.py

        if len(args) == 0:
            return
        elif len(args) == 1:
            if not isinstance(args[0], type(self)):
                logger.warning("Performing a copyFrom from: %s to: %s" % (type(args[0]), type(self)))
            self.copyFrom(args[0])
        else:
            from Ganga.GPIDev.Base.Proxy import TypeMismatchError
            raise TypeMismatchError("Constructor expected one or zero non-keyword arguments, got %i" % len(args))

    @synchronised
    def accept(self, visitor):
        """
        This accepts a VPrinter or VStreamer class instance visitor which is used to display the contents of the object according the Schema
        Args:
            visitor (VPrinter, VStreamer): An instance which will produce a display of this contents of this object
        """

        if not hasattr(self, '_schema'):
            return
        elif self._schema is None:
            visitor.nodeBegin(self)
            visitor.nodeEnd(self)
            return

        visitor.nodeBegin(self)

        for (name, item) in self._schema.simpleItems():
            if item['visitable']:
                if name in self._data:
                    visitor.simpleAttribute(self, name, getattr(self, name), item['sequence'])
                else:
                    visitor.simpleAttribute(self, name, self._schema.getDefaultValue(name, False), item['sequence'])

        for (name, item) in self._schema.sharedItems():
            if item['visitable']:
                if name in self._data:
                    visitor.sharedAttribute(self, name, getattr(self, name), item['sequence'])
                else:
                    visitor.sharedAttribute(self, name, self._schema.getDefaultValue(name, False), item['sequence'])

        for (name, item) in self._schema.componentItems():
            if item['visitable']:
                if name in self._data:
                    visitor.componentAttribute(self, name, getattr(self, name), item['sequence'])
                else:
                    visitor.componentAttribute(self, name, self._schema.getDefaultValue(name, False), item['sequence'])

        visitor.nodeEnd(self)

    def copyFrom(self, srcobj, _ignore_atts=None):
        # type: (GangaObject, Optional[Sequence[str]]) -> None
        """
        copy all the properties recursively from the srcobj
        if schema of self and srcobj are not compatible raises a ValueError
        ON FAILURE LEAVES SELF IN INCONSISTENT STATE
        Args:
            srcobj (GangaObject): This is the ganga object which is to have it's contents from
            _ignore_atts (list): This is a list of attribute names which are to not be copied
        """

        if _ignore_atts is None:
            _ignore_atts = []
        _srcobj = srcobj
        # Check if this object is derived from the source object, then the copy
        # will not throw away information

        if not hasattr(_srcobj, '__class__') and not inspect.isclass(_srcobj.__class__):
            raise GangaValueError("Can't copyFrom a non-class object: %s isclass: %s" % (_srcobj, inspect.isclass(_srcobj)))

        if not isinstance(self, _srcobj.__class__) and not isinstance(_srcobj, self.__class__):
            raise GangaValueError("copyFrom: Cannot copy from %s to %s!" % (_getName(_srcobj), _getName(self)))

        if not hasattr(self, '_schema'):
            logger.debug("No Schema found for myself")
            return

        self._actually_copyFrom(_srcobj, _ignore_atts)

        ## Fix some objects losing parent knowledge
        src_dict = srcobj.__dict__
        for key, val in src_dict.iteritems():
            this_attr = getattr(srcobj, key)
            if isinstance(this_attr, Node) and key not in do_not_copy:
                #logger.debug("k: %s  Parent: %s" % (key, (srcobj)))
                this_attr._setParent(srcobj)

    @synchronised
    def _actually_copyFrom(self, _srcobj, _ignore_atts):
        # type: (GangaObject, Optional[Sequence[str]]) -> None

        for name, obj in _srcobj._data.iteritems():
            item = self._schema.getItem(name)
            if name in _ignore_atts:
                continue

            #logger.debug("Copying: %s : %s" % (name, item))
            if name == 'application' and hasattr(_srcobj.application, 'is_prepared'):
                _app = _srcobj.application
                if _app.is_prepared not in [None, True]:
                    _app.incrementShareCounter(_app.is_prepared.name)

            if not self._schema.hasAttribute(name):
                if not hasattr(self, name):
                    setattr(self, name, self._schema.getDefaultValue(name))
                this_attr = obj
                if isinstance(this_attr, Node) and name not in do_not_copy:
                    this_attr._setParent(self)
            elif not item['copyable']: ## Default of '1' instead of True...
                if not hasattr(self, name):
                    setattr(self, name, self._schema.getDefaultValue(name))
                this_attr = obj
                if isinstance(this_attr, Node) and name not in do_not_copy:
                    this_attr._setParent(self)
            else:
                copy_obj = deepcopy(getattr(_srcobj, name))
                setattr(self, name, copy_obj)

    @synchronised
    def __eq__(self, obj):
        """
        Compare this object to an other object obj
        Args:
            obj (unknown): Compare which self is to be compared to
        """
        if self is obj:
            return True

        if not isinstance(obj, type(self)):
            return False

        # Compare the schemas against each other
        if self._schema is None and obj._schema is None:
            return True  # If they're both `None`
        elif self._schema is None or obj._schema is None:
            return False  # If just one of them is `None`
        elif not self._schema.isEqual(obj._schema):
            return False  # Both have _schema but do not match

        # Check each schema item in turn and check for equality
        for (name, dict_obj) in self._data.iteritems():
            item = self._schema.getItem(name)
            if item['comparable']:
                #logger.info("testing: %s::%s" % (_getName(self), name))
                if dict_obj != getattr(obj, name):
                    #logger.info( "diff: %s::%s" % (_getName(self), name))
                    return False

        not_defined = set(self._schema.allItemNames()) - set(self._data.keys())

        for name in not_defined:
            if obj._schema.hasItem(name):
                if self._schema.getItem(name)['comparable']:
                    if self._schema.getDefaultValue(name, False) != obj._schema.getDefaultValue(name, False):
                        return False
        
        return True

    @synchronised
    def setSchemaAttribute(self, attrib_name, attrib_value):
        # type: (str, Any) -> None
        """
        This sets the value of a schema attribute directly by circumventing the descriptor

        Args:
            attrib_name (str): the name of the schema attribute
            attrib_value (unknown): the value to set it to
        """
        self._data[attrib_name] = attrib_value
        if isinstance(attrib_value, Node):
            self._data[attrib_name]._setParent(self)

    @property
    def _index_cache(self):
        """
        This returns the index cache.
        If this object has been fully loaded into memory and has a Registry assoicated with it it's created dynamically
        If this object isn't fully loaded or has no Registry associated with it the index_cache should be returned whatever it is
        """
        if self._fullyLoadedFromDisk():
            if self._getRegistry() is not None:
                # Fully loaded so lets regenerate this on the fly to avoid losing data
                return self._getRegistry().getIndexCache(self)
            else:
                # No registry therefore can't work out the Cache, probably empty, lets return that
                return self._index_cache_dict
        # Not in registry or not loaded, so can't re-generate if requested
        return self._index_cache_dict

    @_index_cache.setter
    def _index_cache(self, new_index_cache):
        """
        Set the index cache to have some new value which is defined externally.
        (This should __NEVER__ be done on live in-memory objects
        Args:
            new_inde_cache (dict): Dict of new entries for the new_index_cache
        """
        if self._fullyLoadedFromDisk():
            logger.debug("Warning: Setting IndexCache data on live object, please avoid!")
        self._index_cache_dict = new_index_cache

    def _fullyLoadedFromDisk(self):
        # type: () -> bool
        """This returns a boolean. and it's related to if self has_loaded in the Registry of this object"""
        return self._inMemory

    @staticmethod
    def __incrementShareRef(obj, attr_name):
        """
        This increments the shareRef of the prep registry according to the attr_name.name
        Args:
            obj (GangaObject): This is the object which has the attr_name attribute
            attr_name (str): This is the name of the attribute which contains a SharedDir
        """
        shared_dir = getattr(obj, attr_name)

        if hasattr(shared_dir, 'name'):

            from Ganga.Core.GangaRepository import getRegistry
            shareref = getRegistry("prep").getShareRef()

            logger.debug("Increasing shareref")
            shareref.increase(shared_dir.name)

    def __copy__(self):
        cls = self.__class__
        obj = cls()
        # FIXME: this is different than for deepcopy... is this really correct?
        this_dict = copy(self.__dict__)
        for elem in this_dict.keys():
            if elem not in do_not_copy:
                this_dict[elem] = copy(this_dict[elem])
            else:
                this_dict[elem] = None
        obj._setParent(self._getParent())
        obj._index_cache = {}
        obj._registry = self._registry
        return obj

    # on the deepcopy reset all non-copyable properties as defined in the
    # schema
    @synchronised
    def __deepcopy__(self, memo=None):
        """
        Perform a deep copy of the GangaObject class
        Args:
            memo (unknown): Used to track infinite loops etc in the deep-copy of objects
        """
        true_parent = self._getParent()
        cls = self.__class__

        self_copy = cls()

        global do_not_copy
        for name, obj in self._data.iteritems():
            item = self._schema.getItem(name)
            if not item['copyable'] or name in do_not_copy:
                setattr(self_copy, name, self._schema.getDefaultValue(name))
            else:
                if hasattr(self, name):
                    setattr(self_copy, name, deepcopy(obj))
                else:
                   setattr(self_copy, name, self._schema.getDefaultValue(name))

            if item.isA(SharedItem):
                self.__incrementShareRef(self_copy, name)

        for k, v in self.__dict__.iteritems():
            if k not in do_not_copy:
                try:
                    self_copy.__dict__[k] = deepcopy(v)
                except:
                    pass

        if true_parent is not None:
            self._setParent(true_parent)
            self_copy._setParent(true_parent)
        setattr(self_copy, '_registry', self._registry)
        return self_copy

    def clone(self):
        """Clone self and return a properly initialized object"""
        return deepcopy(self)

    def _getIOTimeOut(self):
        """
        Get the DiskIOTimeout or 5 if this is not defined in the config
        """
        from Ganga.Utility.Config.Config import getConfig, ConfigError
        try:
            _timeOut = getConfig('Configuration')['DiskIOTimeout']
        except ConfigError, err:
            _timeOut = 5. # 5sec hardcoded default
        return _timeOut

    def _getWriteAccess(self):
        """ tries to get write access to the object.
        Raise LockingError (or so) on fail """
        root = self._getRoot()
        reg = root._getRegistry()
        if reg is not None:
            _haveLocked = False
            _counter = 1
            _sleep_size = 1
            _timeOut = self._getIOTimeOut()
            while not _haveLocked:
                err = None
                from Ganga.Core.GangaRepository.Registry import RegistryLockError, RegistryAccessError
                reg._write_access(root)
                try:
                    reg._write_access(root)
                    _haveLocked = True
                except (RegistryLockError, RegistryAccessError) as x:
                    #import traceback
                    #traceback.print_stack()
                    from time import sleep
                    sleep(_sleep_size)  # Sleep 2 sec between tests
                    logger.info("Waiting on Write access to registry: %s" % reg.name)
                    logger.debug("err: %s" % x)
                    err = x
                _counter += 1
                # Sleep 2 sec longer than the time taken to bail out
                if _counter * _sleep_size >= _timeOut + 2:
                    logger.error("Failed to get access to registry: %s. Reason: %s" % (reg.name, err))
                    if err is not None:
                        raise err

    def _releaseWriteAccess(self):
        """ releases write access to the object.
        Raise LockingError (or so) on fail
        Please use only if the object is expected to be used by other sessions"""
        root = self._getRoot()
        reg = root._getRegistry()
        if reg is not None:
            logger.debug("Releasing: %s" % (reg.name))
            reg._release_lock(root)

    def _getReadAccess(self):
        """ makes sure the objects _data is there and the object itself has a recent state.
        Raise RepositoryError"""
        root = self._getRoot()
        reg = root._getRegistry()
        if reg is not None:
            reg._read_access(root, self)

    # define when the object is read-only (for example a job is read-only in
    # the states other than new)
    def _readonly(self):
        """
        Returns a 1 or 0 depending on if this object is read-only
        TODO: make this True/False
        """
        r = self._getRoot()
        # is object a root for itself? check needed otherwise infinite
        # recursion
        if r is None or r is self:
            return 0
        else:
            return r._readonly()

    def _setRegistry(self, registry):
        """
        Set the Registry of the GangaObject which will manage it. This can only
        set the registry *to* or *from* None and never from one registry to
        another.
        Args:
            registry (GangaRegistry): This is a Ganga Registry object
        """
        assert self._getParent() is None, 'Can only set the registry of a root object'
        if registry is None or self._registry is None:
            self._registry = registry
        elif registry is not self._registry:
            raise RuntimeError('Cannot set registry of {0} to {1} if one is already set ({2}).'.format(type(self), registry, self._registry))

    # get the registry for the object by getting the registry associated with
    # the root object (if any)
    def _getRegistry(self):
        """
        Get the registry which is managing this GangaObject
        The registry is only managing a root object so it gets this first
        """
        r = self._getRoot()
        return r._registry

    def _getRegistryID(self):
        """
        Get the ID of self within a Registry
        This is normally the .id of an object itself but there is no need for it to be implemented this way
        """
        try:
            return self._registry.find(self)
        except AttributeError, err:
            logger.debug("_getRegistryID Exception: %s" % err)
            return None

    @synchronised
    def _setFlushed(self):
        """Un-Set the dirty flag all of the way down the schema."""
        for k in self._data.keys():
            ## Avoid attributes the likes of job.master which crawl back up the tree
            properties = self._schema[k].getProperties()
            if not properties['visitable'] or properties['transient']:
                continue
            this_attr = getattr(self, k)
            if isinstance(this_attr, Node):
                this_attr._setFlushed()
        super(GangaObject, self)._setFlushed()

    # post __init__ hook automatically called by GPI Proxy __init__
    def _auto__init__(self):
        """
        This is called when an object is constructed from infront of the Proxy automatically, or manually when mimicing the behavior of the IPython prompt
        default behavior is to do nothing
        """
        pass

    # return True if _name attribute was explicitly defined in the class
    # this means that implicit (inherited) _name attribute has no effect in the derived class
    # example: cls._declared_property('hidden') => True if there is class
    # attribute _hidden explicitly declared
    @classmethod
    def _declared_property(cls, name):
        return '_' + name in cls.__dict__

    # get the job object associated with self or raise an assertion error
    # the FIRST PARENT Job is returned...
    # this method is for convenience and may well be moved to some subclass
    def getJobObject(self):
        """
        Return the parent Job which manages this object or throw an AssertionError is non exists
        Unknown: Why is this a GangaObject method and not a Node method?
        """
        from Ganga.GPIDev.Lib.Job import Job
        r = self._getRoot(cond=lambda o: isinstance(o, Job))
        if not isinstance(r, Job):
            raise AssertionError('no job associated with object ' + repr(self))
        return r

    # Customization of the GPI attribute assignment: Attribute Filters
    #
    # Example of usage:
    # if some properties depend on the value of other properties in a complex way such as:
    # changing platform of Gaudi should change the version if it is not supported... etc.
    #
    # Semantics:
    #  gpi_proxy.x = v        --> stripProxy(gpi_proxy)._attribute_filter__set__('x',v)
    #  gpi_proxy.y = [v1,v2]  --> stripProxy(gpi_proxy)._attribute_filter__set__('x',[v1,v2])
    #
    #  is used for *all* kinds of attributes (component and simple)
    #
    # Attribute Filters are used mainly for side effects such as modification of the state of the self object
    # (as described above).
    #
    # Attribute Filter may also perform an additional conversion of the value which is being assigned.
    #
    # Returns the attribute value (converted or original)
    #
    def _attribute_filter__set__(self, name, v):
        if hasattr(v, '_on_attribute__set__'):
            return v._on_attribute__set__(self, name)
        return v


# define the default component object filter:
# obj.x = "Y"   <=> obj.x = Y()


def string_type_shortcut_filter(val, item):
    """
    Filter which allows for "obj.x = "Y"   <=> obj.x = Y()"
    TODO evaluate removing this and the architecture behind it
    """
    if isinstance(val, type('')):
        if item is None:
            raise ValueError('cannot apply default string conversion, probably you are trying to use it in the constructor')
        from Ganga.Utility.Plugin import allPlugins, PluginManagerError
        try:
            obj = allPlugins.find(item['category'], val)()
            obj._auto__init__()
            return obj
        except PluginManagerError as err:
            logger.debug("string_type_shortcut_filter Exception: %s" % err)
            raise ValueError(err)
    return None

# FIXME: change into classmethod (do they inherit?) and then change stripComponentObject to use class instead of
# FIXME: object (object model clearly fails with sequence of Files)
# FIXME: test: ../bin/ganga -c local_lhcb.ini run.py
# TestNativeSpecific.testFileSequence


from .Filters import allComponentFilters
allComponentFilters.setDefault(string_type_shortcut_filter)

#
#
# $Log: not supported by cvs2svn $
# Revision 1.5.2.9  2009/07/14 14:44:17  ebke
# * several bugfixes
# * changed indexing for XML/Pickle
# * introduce index update minimal time of 20 seconds (reduces lag for typing 'jobs')
# * subjob splitting and individual flushing for XML/Pickle
#
# Revision 1.5.2.8  2009/07/13 22:10:53  ebke
# Update for the new GangaRepository:
# * Moved dict interface from Repository to Registry
# * Clearly specified Exceptions to be raised by Repository
# * proper exception handling in Registry
# * moved _writable to _getWriteAccess, introduce _getReadAccess
# * clarified locking, logic in Registry, less in Repository
# * index reading support in XML (no writing, though..)
# * general index reading on registry.keys()
#
# Revision 1.5.2.7  2009/07/10 12:14:10  ebke
# Fixed wrong sequence in __set__: only dirty _after_ writing!
#
# Revision 1.5.2.6  2009/07/10 11:33:06  ebke
# Preparations and fixes for lazy loading
#
# Revision 1.5.2.5  2009/07/08 15:27:50  ebke
# Removed load speed bottleneck for pickle - reduced __setstate__ time by factor 3.
#
# Revision 1.5.2.4  2009/07/08 12:51:52  ebke
# Fixes some bugs introduced in the latest version
#
# Revision 1.5.2.3  2009/07/08 12:36:54  ebke
# Simplified _writable
#
# Revision 1.5.2.2  2009/07/08 11:18:21  ebke
# Initial commit of all - mostly small - modifications due to the new GangaRepository.
# No interface visible to the user is changed
#
# Revision 1.5.2.1  2009/06/04 12:00:37  moscicki
# *** empty log message ***
#
# Revision 1.5  2009/05/20 13:40:22  moscicki
# added filter property for GangaObjects
#
# added Utility.Config.expandgangasystemvars() filter which expands @{VAR} in strings, where VAR is a configuration option defined in the System section
# Usage example: specify @{GANGA_PYTHONPATH} in the configuration file to make pathnames relative to the location of Ganga release; specify @{GANGA_VERSION} to expand to current Ganga version. etc.
#
# modified credentials package (ICommandSet) to use the expandgangasystemvars() filter.
#
# Revision 1.4  2009/04/27 09:22:56  moscicki
# fix #29745: use __mro__ rather than first-generation of base classes
#
# Revision 1.3  2009/02/24 14:57:56  moscicki
# set parent correctly for GangaList items (in __setstate__)
#
# Revision 1.2  2008/09/09 14:37:16  moscicki
# bugfix #40220: Ensure that default values satisfy the declared types in the schema
#
# factored out type checking into schema module, fixed a number of wrongly declared schema items in the core
#
# Revision 1.1  2008/07/17 16:40:52  moscicki
# migration of 5.0.2 to HEAD
#
# the doc and release/tools have been taken from HEAD
#
# Revision 1.27.4.10  2008/03/31 15:30:26  kubam
# More flexible internal logic of hiding the plugin classes derived from GangaObject:
#
# # by default classes are not hidden, config generation and plugin registration is enabled
#
# _hidden       = 1  # optional, specify in the class if you do not want to export it publicly in GPI,
#                    # the class will not be registered as a plugin unless _enable_plugin is defined
#                    # the test if the class is hidden is performed by x._declared_property('hidden')
#
# # additional properties that may be set in derived classes which were declared as _hidden:
# #   _enable_plugin = 1 -> allow registration of _hidden classes in the allPlugins dictionary
# #   _enable_config = 1 -> allow generation of [default_X] configuration section with schema properties
#
# This fixes: bug #34470: config [defaults_GridProxy] missing (issue of _hidden property of GangaObject)
#
# Revision 1.27.4.9  2008/02/28 15:44:31  moscicki
# fixed set parent problem for GangaList (and removed Will's hack which was already commented out)
#
# Revision 1.27.4.8  2008/02/12 09:25:24  amuraru
# removed Will's hack to set the parent, it causes side effects in subjobs accessor(to be checked)
#
# Revision 1.27.4.7  2008/02/06 17:02:00  moscicki
# small fix
#
# Revision 1.27.4.6  2008/02/06 13:00:21  wreece
# Adds a bit of a HACK as a tempory measure. The parent of a GangaList is being lost somewhere (I suspect due to a copy). I've added it back manually in __get__.
#
# Revision 1.27.4.5  2008/02/06 09:28:48  wreece
# First pass at a cleanup of the gangalist stuff. I've made changes so the diffs with the 4.4 series are more transparent. Currently still test failures.
#
# Revision 1.27.4.4  2007/12/18 09:05:04  moscicki
# integrated typesystem from Alvin and made more uniform error reporting
#
# Revision 1.27.4.3  2007/11/14 13:03:54  wreece
# Changes to make shortcuts work correctly with gangalists. all but one tests should now pass.
#
# Revision 1.27.4.2  2007/11/07 15:10:02  moscicki
# merged in pretty print and GangaList support from ganga-5-dev-branch-4-4-1-will-print branch
#
#
# Revision 1.27.4.1  2007/10/30 15:25:53  moscicki
# fixed #29745: Inherited functions of GangaObjects cannot be exported via _exportmethods
#
# Revision 1.27.8.3  2007/10/30 21:22:02  wreece
# Numerous small fixes and work arounds. And a new test.
#
# Revision 1.27.8.2  2007/10/30 14:30:23  wreece
# Non-working update. Adds in Kuba's exported methods dodge. It is now possible to define a _export_ version of a method for external use and a undecorated method for internal use.
#
# Revision 1.27.8.1  2007/10/30 12:12:08  wreece
# First version of the new print_summary functionality. Lots of changes, but some known limitations. Will address in next version.
#
# Revision 1.27  2007/07/27 13:52:00  moscicki
# merger updates from Will (from GangaMergers-1-0 branch)
#
# Revision 1.26.12.1  2007/05/14 13:32:11  wreece
# Adds the merger related code on a seperate branch. All tests currently
# run successfully.
#
# Revision 1.26  2006/07/27 20:09:54  moscicki
# _getJobObject() renamed -> getJobObject() and finding FIRST PARENT JOB
# _getRoot() : cond optional argument (to cut the search path e.g. for getJobObject())
#
# getDefaultValue() moved to Schema object
#
# "checkset" metaproperty implemented in schema (to check the direct updates to job.status)
# modified the "getter" metaproperty implementation
# create automatically the configuration units with default property values
#
# Revision 1.25  2006/02/10 14:18:44  moscicki
# removed obsoleted eval for default properties from config file
#
# Revision 1.24  2006/01/09 16:36:55  moscicki
#  - support for defining default properties in the configuration
#    config file example:
#
#      [LSF_Properties]
#      queue = myQueue
#
#      [LCG_Properties]
#      requirements.CE = myCE
#
#      [Job_Properties]
#      application = DaVinci
#      application.version = v99r2
#
# Revision 1.23  2005/12/02 15:27:13  moscicki
# support for "visitable" metaproperty
# support for hidden GPI classes
# "hidden" properties not visible in the proxies
# support for 'getter' type of property (a binding) for job.master
#
# Revision 1.22  2005/11/14 10:29:55  moscicki
# adapted to changed interface of allPlugins.add() method
#
# Revision 1.21  2005/11/01 16:43:51  moscicki
# added isStringLike condition to avoid unnecesary looping over strings
#
# Revision 1.20  2005/11/01 14:04:55  moscicki
# added missing implementation of GangaObject.__setstate__
# fixed the implementation of Node.__setstate__ to correctly set parent for objects which are contained in iterable simple items (lists, dictionaries) etc. (contributed by AS)
#
# Revision 1.19  2005/11/01 11:09:48  moscicki
# changes to support import/export (KH):
#   - The printTree method accepts an additional argument, which
#     it passes on to VPrinter as the value for "selection".
#
# Revision 1.18  2005/08/26 09:53:24  moscicki
# copy __doc__ for exported method
# _getJobObject() helper method in GangaObject
#
# Revision 1.17  2005/08/24 15:41:19  moscicki
# automatically generated help for properties, disabled the SchemaHelper and few other improvements to the help system
#
# Revision 1.16  2005/08/23 17:15:06  moscicki
# *** empty log message ***
#
#
#
