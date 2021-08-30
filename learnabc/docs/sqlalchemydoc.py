"""
Here, the Object Relational Mapper is introduced and fully described. If you want to work with higher-level SQL
which is constructed automatically for you, as well as automated persistence of Python objects, proceed first to the
tutorial.
2.1 Object Relational Tutorial
The SQLAlchemy Object Relational Mapper presents a method of associating user-defined Python classes with
database tables, and instances of those classes (objects) with rows in their corresponding tables. It includes a system that transparently synchronizes all changes in state between objects and their related rows, called a unit of work,
as well as a system for expressing database queries in terms of the user defined classes and their defined relationships
between each other.
The ORM is in contrast to the SQLAlchemy Expression Language, upon which the ORM is constructed. Whereas the
SQL Expression Language, introduced in SQL Expression Language Tutorial, presents a system of representing the
primitive constructs of the relational database directly without opinion, the ORM presents a high level and abstracted
pattern of usage, which itself is an example of applied usage of the Expression Language.
While there is overlap among the usage patterns of the ORM and the Expression Language, the similarities are more
superficial than they may at first appear. One approaches the structure and content of data from the perspective of
a user-defined domain model which is transparently persisted and refreshed from its underlying storage model. The
other approaches it from the perspective of literal schema and SQL expression representations which are explicitly
composed into messages consumed individually by the database.
A successful application may be constructed using the Object Relational Mapper exclusively. In advanced situations,
an application constructed with the ORM may make occasional usage of the Expression Language directly in certain
areas where specific database interactions are required.
The following tutorial is in doctest format, meaning each >>> line represents something you can type at a Python
command prompt, and the following text represents the expected return value.
2.1.1 Version Check
A quick check to verify that we are on at least version 0.9 of SQLAlchemy:
>>> import sqlalchemy
>>> sqlalchemy.__version__
0.9.0
7
SQLAlchemy Documentation, Release 0.9.10
2.1.2 Connecting
For this tutorial we will use an in-memory-only SQLite database. To connect we use create_engine():
>>> from sqlalchemy import create_engine
>>> engine = create_engine('sqlite:///:memory:', echo=True)
The echo flag is a shortcut to setting up SQLAlchemy logging, which is accomplished via Python’s standard
logging module. With it enabled, we’ll see all the generated SQL produced. If you are working through this
tutorial and want less output generated, set it to False. This tutorial will format the SQL behind a popup window so
it doesn’t get in our way; just click the “SQL” links to see what’s being generated.
The return value of create_engine() is an instance of Engine, and it represents the core interface to the
database, adapted through a dialect that handles the details of the database and DBAPI in use. In this case the SQLite
dialect will interpret instructions to the Python built-in sqlite3 module.
Lazy Connecting
The Engine, when first returned by create_engine(), has not actually tried to connect to the database
yet; that happens only the first time it is asked to perform a task against the database.
The first time a method like Engine.execute() or Engine.connect() is called, the Engine establishes a
real DBAPI connection to the database, which is then used to emit the SQL. When using the ORM, we typically don’t
use the Engine directly once created; instead, it’s used behind the scenes by the ORM as we’ll see shortly.
See also:
Database Urls - includes examples of create_engine() connecting to several kinds of databases with links to
more information.
2.1.3 Declare a Mapping
When using the ORM, the configurational process starts by describing the database tables we’ll be dealing with, and
then by defining our own classes which will be mapped to those tables. In modern SQLAlchemy, these two tasks
are usually performed together, using a system known as Declarative, which allows us to create classes that include
directives to describe the actual database table they will be mapped to.
Classes mapped using the Declarative system are defined in terms of a base class which maintains a catalog of classes
and tables relative to that base - this is known as the declarative base class. Our application will usually have just one
instance of this base in a commonly imported module. We create the base class using the declarative_base()
function, as follows:
>>> from sqlalchemy.ext.declarative import declarative_base
>>> Base = declarative_base()
Now that we have a “base”, we can define any number of mapped classes in terms of it. We will start with just a single
table called users, which will store records for the end-users using our application. A new class called User will
be the class to which we map this table. Within the class, we define details about the table to which we’ll be mapping,
primarily the table name, and names and datatypes of columns:
>>> from sqlalchemy import Column, Integer, String
>>> class User(Base):
... __tablename__ = 'users'
...
... id = Column(Integer, primary_key=True)
8 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
... name = Column(String)
... fullname = Column(String)
... password = Column(String)
...
... def __repr__(self):
... return "<User(name='%s', fullname='%s', password='%s')>" % (
... self.name, self.fullname, self.password)
Tip
The User class defines a __repr__() method, but note that is optional; we only implement it in this tutorial
so that our examples show nicely formatted User objects.
A class using Declarative at a minimum needs a __tablename__ attribute, and at least one Column which is part of
a primary key 1
. SQLAlchemy never makes any assumptions by itself about the table to which a class refers, including
that it has no built-in conventions for names, datatypes, or constraints. But this doesn’t mean boilerplate is required;
instead, you’re encouraged to create your own automated conventions using helper functions and mixin classes, which
is described in detail at Mixin and Custom Base Classes.
When our class is constructed, Declarative replaces all the Column objects with special Python accessors known as
descriptors; this is a process known as instrumentation. The “instrumented” mapped class will provide us with the
means to refer to our table in a SQL context as well as to persist and load the values of columns from the database.
Outside of what the mapping process does to our class, the class remains otherwise mostly a normal Python class, to
which we can define any number of ordinary attributes and methods needed by our application.
2.1.4 Create a Schema
With our User class constructed via the Declarative system, we have defined information about our table, known as
table metadata. The object used by SQLAlchemy to represent this information for a specific table is called the Table
object, and here Declarative has made one for us. We can see this object by inspecting the __table__ attribute:
>>> User.__table__
Table('users', MetaData(bind=None),
Column('id', Integer(), table=<users>, primary_key=True, nullable=False),
Column('name', String(), table=<users>),
Column('fullname', String(), table=<users>),
Column('password', String(), table=<users>), schema=None)
Classical Mappings
The Declarative system, though highly recommended, is not required in order to use SQLAlchemy’s ORM.
Outside of Declarative, any plain Python class can be mapped to any Table using the mapper() function
directly; this less common usage is described at Classical Mappings.
When we declared our class, Declarative used a Python metaclass in order to perform additional activities once the
class declaration was complete; within this phase, it then created a Table object according to our specifications, and
associated it with the class by constructing a Mapper object. This object is a behind-the-scenes object we normally
don’t need to deal with directly (though it can provide plenty of information about our mapping when we need it).
The Table object is a member of a larger collection known as MetaData. When using Declarative, this object is
available using the .metadata attribute of our declarative base class.
1 For information on why a primary key is required, see How do I map a table that has no primary key?.
2.1. Object Relational Tutorial 9
SQLAlchemy Documentation, Release 0.9.10
The MetaData is a registry which includes the ability to emit a limited set of schema generation commands to
the database. As our SQLite database does not actually have a users table present, we can use MetaData
to issue CREATE TABLE statements to the database for all tables that don’t yet exist. Below, we call the
MetaData.create_all() method, passing in our Engine as a source of database connectivity. We will see
that special commands are first emitted to check for the presence of the users table, and following that the actual
CREATE TABLE statement:
>>> Base.metadata.create_all(engine) # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
PRAGMA table_info("users")
()
CREATE TABLE users (
id INTEGER NOT NULL,
name VARCHAR,
fullname VARCHAR,
password VARCHAR,
PRIMARY KEY (id)
)
()
COMMIT
Minimal Table Descriptions vs. Full Descriptions
Users familiar with the syntax of CREATE TABLE may notice that the VARCHAR columns were generated
without a length; on SQLite and Postgresql, this is a valid datatype, but on others, it’s not allowed. So if running
this tutorial on one of those databases, and you wish to use SQLAlchemy to issue CREATE TABLE, a “length”
may be provided to the String type as below:
Column(String(50))
The length field on String, as well as similar precision/scale fields available on Integer, Numeric, etc.
are not referenced by SQLAlchemy other than when creating tables.
Additionally, Firebird and Oracle require sequences to generate new primary key identifiers, and SQLAlchemy
doesn’t generate or assume these without being instructed. For that, you use the Sequence construct:
from sqlalchemy import Sequence
Column(Integer, Sequence('user_id_seq'), primary_key=True)
A full, foolproof Table generated via our declarative mapping is therefore:
class User(Base):
__tablename__ = 'users'
id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
name = Column(String(50))
fullname = Column(String(50))
password = Column(String(12))
def __repr__(self):
return "<User(name='%s', fullname='%s', password='%s')>" % (
self.name, self.fullname, self.password)
We include this more verbose table definition separately to highlight the difference between a minimal construct
geared primarily towards in-Python usage only, versus one that will be used to emit CREATE TABLE statements
on a particular set of backends with more stringent requirements.
2.1.5 Create an Instance of the Mapped Class
With mappings complete, let’s now create and inspect a User object:
10 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> ed_user.name
'ed'
>>> ed_user.password
'edspassword'
>>> str(ed_user.id)
'None'
the __init__() method
Our User class, as defined using the Declarative system, has been provided with a constructor (e.g.
__init__() method) which automatically accepts keyword names that match the columns we’ve mapped.
We are free to define any explicit __init__() method we prefer on our class, which will override the default
method provided by Declarative.
Even though we didn’t specify it in the constructor, the id attribute still produces a value of None when we access
it (as opposed to Python’s usual behavior of raising AttributeError for an undefined attribute). SQLAlchemy’s
instrumentation normally produces this default value for column-mapped attributes when first accessed. For those
attributes where we’ve actually assigned a value, the instrumentation system is tracking those assignments for use
within an eventual INSERT statement to be emitted to the database.
2.1.6 Creating a Session
We’re now ready to start talking to the database. The ORM’s “handle” to the database is the Session. When we first
set up the application, at the same level as our create_engine() statement, we define a Session class which
will serve as a factory for new Session objects:
>>> from sqlalchemy.orm import sessionmaker
>>> Session = sessionmaker(bind=engine)
In the case where your application does not yet have an Engine when you define your module-level objects, just set
it up like this:
>>> Session = sessionmaker()
Later, when you create your engine with create_engine(), connect it to the Session using configure():
>>> Session.configure(bind=engine) # once engine is available
Session Lifecycle Patterns
The question of when to make a Session depends a lot on what kind of application is being built. Keep in
mind, the Session is just a workspace for your objects, local to a particular database connection - if you think
of an application thread as a guest at a dinner party, the Session is the guest’s plate and the objects it holds are
the food (and the database...the kitchen?)! More on this topic available at When do I construct a Session, when
do I commit it, and when do I close it?.
This custom-made Session class will create new Session objects which are bound to our database. Other transactional characteristics may be defined when calling sessionmaker as well; these are described in a later chapter.
Then, whenever you need to have a conversation with the database, you instantiate a Session:
>>> session = Session()
2.1. Object Relational Tutorial 11
SQLAlchemy Documentation, Release 0.9.10
The above Session is associated with our SQLite-enabled Engine, but it hasn’t opened any connections yet. When
it’s first used, it retrieves a connection from a pool of connections maintained by the Engine, and holds onto it until
we commit all changes and/or close the session object.
2.1.7 Adding and Updating Objects
To persist our User object, we add() it to our Session:
>>> ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
>>> session.add(ed_user)
At this point, we say that the instance is pending; no SQL has yet been issued and the object is not yet represented by
a row in the database. The Session will issue the SQL to persist Ed Jones as soon as is needed, using a process
known as a flush. If we query the database for Ed Jones, all pending information will first be flushed, and the query
is issued immediately thereafter.
For example, below we create a new Query object which loads instances of User. We “filter by” the name attribute
of ed, and indicate that we’d like only the first result in the full list of rows. A User instance is returned which is
equivalent to that which we’ve added:
>>> our_user = session.query(User).filter_by(name='ed').first() # doctest:+ELLIPSIS,+NORMALIZE_WHITESPACE
BEGIN (implicit)
INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
('ed', 'Ed Jones', 'edspassword')
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name = ?
LIMIT ? OFFSET ?
('ed', 1, 0)
>>> our_user
<User(name='ed', fullname='Ed Jones', password='edspassword')>
In fact, the Session has identified that the row returned is the same row as one already represented within its internal
map of objects, so we actually got back the identical instance as that which we just added:
>>> ed_user is our_user
True
The ORM concept at work here is known as an identity map and ensures that all operations upon a particular row
within a Session operate upon the same set of data. Once an object with a particular primary key is present in the
Session, all SQL queries on that Session will always return the same Python object for that particular primary
key; it also will raise an error if an attempt is made to place a second, already-persisted object with the same primary
key within the session.
We can add more User objects at once using add_all():
>>> session.add_all([
... User(name='wendy', fullname='Wendy Williams', password='foobar'),
... User(name='mary', fullname='Mary Contrary', password='xxg527'),
... User(name='fred', fullname='Fred Flinstone', password='blah')])
Also, we’ve decided the password for Ed isn’t too secure, so lets change it:
>>> ed_user.password = 'f8s7ccs'
The Session is paying attention. It knows, for example, that Ed Jones has been modified:
12 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
>>> session.dirty
IdentitySet([<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>])
and that three new User objects are pending:
>>> session.new # doctest: +SKIP
IdentitySet([<User(name='wendy', fullname='Wendy Williams', password='foobar')>,
<User(name='mary', fullname='Mary Contrary', password='xxg527')>,
<User(name='fred', fullname='Fred Flinstone', password='blah')>])
We tell the Session that we’d like to issue all remaining changes to the database and commit the transaction, which
has been in progress throughout. We do this via commit(). The Session emits the UPDATE statement for the
password change on “ed”, as well as INSERT statements for the three new User objects we’ve added:
>>> session.commit()
UPDATE users SET password=? WHERE users.id = ?
('f8s7ccs', 1)
INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
('wendy', 'Wendy Williams', 'foobar')
INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
('mary', 'Mary Contrary', 'xxg527')
INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
('fred', 'Fred Flinstone', 'blah')
COMMIT
commit() flushes whatever remaining changes remain to the database, and commits the transaction. The connection
resources referenced by the session are now returned to the connection pool. Subsequent operations with this session
will occur in a new transaction, which will again re-acquire connection resources when first needed.
If we look at Ed’s id attribute, which earlier was None, it now has a value:
>>> ed_user.id # doctest: +NORMALIZE_WHITESPACE
BEGIN (implicit)
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.id = ?
(1,)
1
After the Session inserts new rows in the database, all newly generated identifiers and database-generated defaults
become available on the instance, either immediately or via load-on-first-access. In this case, the entire row was reloaded on access because a new transaction was begun after we issued commit(). SQLAlchemy by default refreshes
data from a previous transaction the first time it’s accessed within a new transaction, so that the most recent state is
available. The level of reloading is configurable as is described in Using the Session.
Session Object States
As our User object moved from being outside the Session, to inside the Session without a primary key, to
actually being inserted, it moved between three out of four available “object states” - transient, pending, and
persistent. Being aware of these states and what they mean is always a good idea - be sure to read Quickie Intro
to Object States for a quick overview.
2.1. Object Relational Tutorial 13
SQLAlchemy Documentation, Release 0.9.10
2.1.8 Rolling Back
Since the Session works within a transaction, we can roll back changes made too. Let’s make two changes that
we’ll revert; ed_user‘s user name gets set to Edwardo:
>>> ed_user.name = 'Edwardo'
and we’ll add another erroneous user, fake_user:
>>> fake_user = User(name='fakeuser', fullname='Invalid', password='12345')
>>> session.add(fake_user)
Querying the session, we can see that they’re flushed into the current transaction:
>>> session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all() #doctest: +NORMALIZE_WHITESPACE
UPDATE users SET name=? WHERE users.id = ?
('Edwardo', 1)
INSERT INTO users (name, fullname, password) VALUES (?, ?, ?)
('fakeuser', 'Invalid', '12345')
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name IN (?, ?)
('Edwardo', 'fakeuser')
[<User(name='Edwardo', fullname='Ed Jones', password='f8s7ccs')>, <User(user='fakeuser', fullname='Invalid', password='12345')>]
Rolling back, we can see that ed_user‘s name is back to ed, and fake_user has been kicked out of the session:
>>> session.rollback()
ROLLBACK
>>> ed_user.name #doctest: +NORMALIZE_WHITESPACE
BEGIN (implicit)
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.id = ?
(1,)
u'ed'
>>> fake_user in session
False
issuing a SELECT illustrates the changes made to the database:
>>> session.query(User).filter(User.name.in_(['ed', 'fakeuser'])).all() #doctest: +NORMALIZE_WHITESPACE
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name IN (?, ?)
('ed', 'fakeuser')
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>]
14 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
2.1.9 Querying
A Query object is created using the query() method on Session. This function takes a variable number of
arguments, which can be any combination of classes and class-instrumented descriptors. Below, we indicate a Query
which loads User instances. When evaluated in an iterative context, the list of User objects present is returned:
>>> for instance in session.query(User).order_by(User.id): # doctest: +NORMALIZE_WHITESPACE
... print instance.name, instance.fullname
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users ORDER BY users.id
()
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
The Query also accepts ORM-instrumented descriptors as arguments. Any time multiple class entities or columnbased entities are expressed as arguments to the query() function, the return result is expressed as tuples:
>>> for name, fullname in session.query(User.name, User.fullname): # doctest: +NORMALIZE_WHITESPACE
... print name, fullname
SELECT users.name AS users_name,
users.fullname AS users_fullname
FROM users
()
ed Ed Jones
wendy Wendy Williams
mary Mary Contrary
fred Fred Flinstone
The tuples returned by Query are named tuples, supplied by the KeyedTuple class, and can be treated much like
an ordinary Python object. The names are the same as the attribute’s name for an attribute, and the class name for a
class:
>>> for row in session.query(User, User.name).all(): #doctest: +NORMALIZE_WHITESPACE
... print row.User, row.name
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
()
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')> ed
<User(name='wendy', fullname='Wendy Williams', password='foobar')> wendy
<User(name='mary', fullname='Mary Contrary', password='xxg527')> mary
<User(name='fred', fullname='Fred Flinstone', password='blah')> fred
You can control the names of individual column expressions using the label() construct, which is available from
any ColumnElement-derived object, as well as any class attribute which is mapped to one (such as User.name):
>>> for row in session.query(User.name.label('name_label')).all(): #doctest: +NORMALIZE_WHITESPACE
... print(row.name_label)
SELECT users.name AS name_label
FROM users
()
ed
2.1. Object Relational Tutorial 15
SQLAlchemy Documentation, Release 0.9.10
wendy
mary
fred
The name given to a full entity such as User, assuming that multiple entities are present in the call to query(), can
be controlled using aliased() :
>>> from sqlalchemy.orm import aliased
>>> user_alias = aliased(User, name='user_alias')
>>> for row in session.query(user_alias, user_alias.name).all(): #doctest: +NORMALIZE_WHITESPACE
... print row.user_alias
SELECT user_alias.id AS user_alias_id,
user_alias.name AS user_alias_name,
user_alias.fullname AS user_alias_fullname,
user_alias.password AS user_alias_password
FROM users AS user_alias
()
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
<User(name='fred', fullname='Fred Flinstone', password='blah')>
Basic operations with Query include issuing LIMIT and OFFSET, most conveniently using Python array slices and
typically in conjunction with ORDER BY:
>>> for u in session.query(User).order_by(User.id)[1:3]: #doctest: +NORMALIZE_WHITESPACE
... print u
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users ORDER BY users.id
LIMIT ? OFFSET ?
(2, 1)
<User(name='wendy', fullname='Wendy Williams', password='foobar')>
<User(name='mary', fullname='Mary Contrary', password='xxg527')>
and filtering results, which is accomplished either with filter_by(), which uses keyword arguments:
>>> for name, in session.query(User.name).\
... filter_by(fullname='Ed Jones'): # doctest: +NORMALIZE_WHITESPACE
... print name
SELECT users.name AS users_name FROM users
WHERE users.fullname = ?
('Ed Jones',)
ed
...or filter(), which uses more flexible SQL expression language constructs. These allow you to use regular
Python operators with the class-level attributes on your mapped class:
>>> for name, in session.query(User.name).\
... filter(User.fullname=='Ed Jones'): # doctest: +NORMALIZE_WHITESPACE
... print name
SELECT users.name AS users_name FROM users
WHERE users.fullname = ?
('Ed Jones',)
ed
The Query object is fully generative, meaning that most method calls return a new Query object upon which
16 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
further criteria may be added. For example, to query for users named “ed” with a full name of “Ed Jones”, you can
call filter() twice, which joins criteria using AND:
>>> for user in session.query(User).\
... filter(User.name=='ed').\
... filter(User.fullname=='Ed Jones'): # doctest: +NORMALIZE_WHITESPACE
... print user
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name = ? AND users.fullname = ?
('ed', 'Ed Jones')
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
Common Filter Operators
Here’s a rundown of some of the most common operators used in filter():
• equals:
query.filter(User.name == 'ed')
• not equals:
query.filter(User.name != 'ed')
• LIKE:
query.filter(User.name.like('%ed%'))
• IN:
query.filter(User.name.in_(['ed', 'wendy', 'jack']))
# works with query objects too:
query.filter(User.name.in_(
session.query(User.name).filter(User.name.like('%ed%'))
))
• NOT IN:
query.filter(~User.name.in_(['ed', 'wendy', 'jack']))
• IS NULL:
query.filter(User.name == None)
# alternatively, if pep8/linters are a concern
query.filter(User.name.is_(None))
• IS NOT NULL:
query.filter(User.name != None)
# alternatively, if pep8/linters are a concern
query.filter(User.name.isnot(None))
• AND:
2.1. Object Relational Tutorial 17
SQLAlchemy Documentation, Release 0.9.10
# use and_()
from sqlalchemy import and_
query.filter(and_(User.name == 'ed', User.fullname == 'Ed Jones'))
# or send multiple expressions to .filter()
query.filter(User.name == 'ed', User.fullname == 'Ed Jones')
# or chain multiple filter()/filter_by() calls
query.filter(User.name == 'ed').filter(User.fullname == 'Ed Jones')
Note: Make sure you use and_() and not the Python and operator!
• OR:
from sqlalchemy import or_
query.filter(or_(User.name == 'ed', User.name == 'wendy'))
Note: Make sure you use or_() and not the Python or operator!
• MATCH:
query.filter(User.name.match('wendy'))
Note: match() uses a database-specific MATCH or CONTAINS function; its behavior will vary by
backend and is not available on some backends such as SQLite.
Returning Lists and Scalars
A number of methods on Query immediately issue SQL and return a value containing loaded database results. Here’s
a brief tour:
• all() returns a list:
>>> query = session.query(User).filter(User.name.like('%ed')).order_by(User.id)
>>> query.all() #doctest: +NORMALIZE_WHITESPACE
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name LIKE ? ORDER BY users.id
('%ed',)
[<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>,
<User(name='fred', fullname='Fred Flinstone', password='blah')>]
• first() applies a limit of one and returns the first result as a scalar:
>>> query.first() #doctest: +NORMALIZE_WHITESPACE
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
18 Chapter 2. SQLAlchemy ORM
SQLAlchemy Documentation, Release 0.9.10
WHERE users.name LIKE ? ORDER BY users.id
LIMIT ? OFFSET ?
('%ed', 1, 0)
<User(name='ed', fullname='Ed Jones', password='f8s7ccs')>
• one(), fully fetches all rows, and if not exactly one object identity or composite row is present in the result,
raises an error. With multiple rows found:
>>> from sqlalchemy.orm.exc import MultipleResultsFound
>>> try: #doctest: +NORMALIZE_WHITESPACE
... user = query.one()
... except MultipleResultsFound, e:
... print e
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name LIKE ? ORDER BY users.id
('%ed',)
Multiple rows were found for one()
With no rows found:
>>> from sqlalchemy.orm.exc import NoResultFound
>>> try: #doctest: +NORMALIZE_WHITESPACE
... user = query.filter(User.id == 99).one()
... except NoResultFound, e:
... print e
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE users.name LIKE ? AND users.id = ? ORDER BY users.id
('%ed', 99)
No row was found for one()
The one() method is great for systems that expect to handle “no items found” versus “multiple items found”
differently; such as a RESTful web service, which may want to raise a “404 not found” when no results are
found, but raise an application error when multiple results are found.
• scalar() invokes the one() method, and upon success returns the first column of the row:
>>> query = session.query(User.id).filter(User.name == 'ed').\
... order_by(User.id)
>>> query.scalar() #doctest: +NORMALIZE_WHITESPACE
SELECT users.id AS users_id
FROM users
WHERE users.name = ? ORDER BY users.id
('ed',)
1
Using Textual SQL
Literal strings can be used flexibly with Query, by specifying their use with the text() construct, which is accepted
by most applicable methods. For example, filter() and order_by():
2.1. Object Relational Tutorial 19
SQLAlchemy Documentation, Release 0.9.10
>>> from sqlalchemy import text
>>> for user in session.query(User).\
... filter(text("id<224")).\
... order_by(text("id")).all(): #doctest: +NORMALIZE_WHITESPACE
... print user.name
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE id<224 ORDER BY id
()
ed
wendy
mary
fred
Bind parameters can be specified with string-based SQL, using a colon. To specify the values, use the params()
method:
>>> session.query(User).filter(text("id<:value and name=:name")).\
... params(value=224, name='fred').order_by(User.id).one() # doctest: +NORMALIZE_WHITESPACE
SELECT users.id AS users_id,
users.name AS users_name,
users.fullname AS users_fullname,
users.password AS users_password
FROM users
WHERE id<? and name=? ORDER BY users.id
(224, 'fred')
<User(name='fred', fullname='Fred Flinstone', password='blah')>
"""
