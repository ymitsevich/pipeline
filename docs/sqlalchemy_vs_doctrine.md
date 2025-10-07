# SQLAlchemy vs Doctrine ORM: Comparison

Both are mature, powerful ORMs that implement similar design patterns. Here's a detailed comparison.

## Overview

| Feature | SQLAlchemy (Python) | Doctrine (PHP) |
|---------|---------------------|----------------|
| **Language** | Python | PHP |
| **First Release** | 2006 | 2008 (Doctrine 2) |
| **Maturity** | Very mature | Very mature |
| **Philosophy** | Pythonic, explicit | Enterprise-focused |
| **Documentation** | Excellent | Excellent |

---

## Architecture Comparison

### Both Implement the Same Patterns ✅

| Pattern | SQLAlchemy | Doctrine |
|---------|------------|----------|
| **Unit of Work** | ✅ Session | ✅ EntityManager |
| **Identity Map** | ✅ Session cache | ✅ First-level cache |
| **Data Mapper** | ✅ Yes | ✅ Yes |
| **Repository** | ⚠️ Can build | ✅ Built-in |
| **Lazy Loading** | ✅ Yes | ✅ Yes |
| **Query Builder** | ✅ Yes | ✅ DQL + QueryBuilder |

---

## Side-by-Side Code Comparison

### 1. Defining Models

**SQLAlchemy:**
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
    
    # Relationship
    orders = relationship("Order", back_populates="user")
```

**Doctrine:**
```php
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity]
#[ORM\Table(name: "users")]
class User
{
    #[ORM\Id]
    #[ORM\Column(type: "integer")]
    #[ORM\GeneratedValue]
    private int $id;
    
    #[ORM\Column(type: "string", length: 50)]
    private string $username;
    
    #[ORM\Column(type: "string", length: 100, unique: true)]
    private string $email;
    
    #[ORM\OneToMany(targetEntity: Order::class, mappedBy: "user")]
    private Collection $orders;
}
```

**Similarities:**
- ✅ Declarative syntax
- ✅ Attributes/decorators for metadata
- ✅ Explicit table and column definitions
- ✅ Relationship mapping

---

### 2. Creating & Persisting Objects

**SQLAlchemy:**
```python
from src.pipeline.database import get_session, User

session = get_session()

# Create
user = User(username="alice", email="alice@example.com")

# Add to Unit of Work
session.add(user)

# Commit (executes SQL)
session.commit()

session.close()
```

**Doctrine:**
```php
$entityManager = EntityManager::create($connection, $config);

// Create
$user = new User();
$user->setUsername("alice");
$user->setEmail("alice@example.com");

// Add to Unit of Work
$entityManager->persist($user);

// Commit (executes SQL)
$entityManager->flush();

$entityManager->clear();
```

**Key Difference:**
- SQLAlchemy: `session.add()` + `session.commit()`
- Doctrine: `persist()` + `flush()`

---

### 3. Querying

**SQLAlchemy:**
```python
# Simple query
users = session.query(User).all()

# With filter
user = session.query(User).filter(User.username == "alice").first()

# With JOIN
from sqlalchemy import join
results = session.query(User, Order).join(Order).all()

# Aggregate
from sqlalchemy import func
count = session.query(func.count(User.id)).scalar()
```

**Doctrine:**
```php
// Simple query
$users = $entityManager->getRepository(User::class)->findAll();

// With filter
$user = $entityManager->getRepository(User::class)
    ->findOneBy(['username' => 'alice']);

// DQL (Doctrine Query Language)
$query = $entityManager->createQuery(
    'SELECT u, o FROM User u JOIN u.orders o WHERE u.username = :name'
);
$query->setParameter('name', 'alice');
$results = $query->getResult();

// QueryBuilder (fluent interface)
$qb = $entityManager->createQueryBuilder();
$users = $qb->select('u')
    ->from(User::class, 'u')
    ->where('u.username = :name')
    ->setParameter('name', 'alice')
    ->getQuery()
    ->getResult();

// Aggregate
$count = $entityManager->createQuery(
    'SELECT COUNT(u.id) FROM User u'
)->getSingleScalarResult();
```

**Key Difference:**
- SQLAlchemy: Direct Python expressions `User.username == "alice"`
- Doctrine: DQL strings or QueryBuilder API

---

### 4. Relationships

**SQLAlchemy:**
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

# Usage
user = session.query(User).first()
for order in user.orders:  # Lazy loads
    print(order.amount)
```

**Doctrine:**
```php
#[ORM\Entity]
class User
{
    #[ORM\OneToMany(targetEntity: Order::class, mappedBy: "user")]
    private Collection $orders;
}

#[ORM\Entity]
class Order
{
    #[ORM\ManyToOne(targetEntity: User::class, inversedBy: "orders")]
    #[ORM\JoinColumn(name: "user_id", referencedColumnName: "id")]
    private User $user;
}

// Usage
$user = $entityManager->find(User::class, 1);
foreach ($user->getOrders() as $order) {  // Lazy loads
    echo $order->getAmount();
}
```

**Similarities:**
- ✅ Both support One-to-Many, Many-to-One, Many-to-Many
- ✅ Both have lazy loading by default
- ✅ Both have eager loading options

---

### 5. Transactions & Unit of Work

**SQLAlchemy:**
```python
session = get_session()
try:
    user = User(username="alice")
    order = Order(user_id=user.id, amount=100.0)
    
    session.add(user)
    session.add(order)
    session.commit()  # Both INSERT execute
except Exception:
    session.rollback()  # Both rollback
finally:
    session.close()
```

**Doctrine:**
```php
$em = $entityManager;
try {
    $user = new User();
    $user->setUsername("alice");
    
    $order = new Order();
    $order->setUser($user);
    $order->setAmount(100.0);
    
    $em->persist($user);
    $em->persist($order);
    $em->flush();  // Both INSERT execute
} catch (Exception $e) {
    // Automatically rolls back on exception
}
```

**Key Difference:**
- SQLAlchemy: Explicit `rollback()` needed
- Doctrine: Auto-rollback on exceptions

---

## Key Differences

### 1. **Repository Pattern**

**Doctrine:** Built-in Repository pattern
```php
class UserRepository extends EntityRepository
{
    public function findActiveUsers(): array
    {
        return $this->createQueryBuilder('u')
            ->where('u.active = :active')
            ->setParameter('active', true)
            ->getQuery()
            ->getResult();
    }
}

// Usage
$userRepo = $em->getRepository(User::class);
$activeUsers = $userRepo->findActiveUsers();
```

**SQLAlchemy:** No built-in repositories, but you can create them:
```python
class UserRepository:
    def __init__(self, session):
        self.session = session
    
    def find_active_users(self):
        return self.session.query(User).filter(User.active == True).all()

# Usage
repo = UserRepository(session)
active_users = repo.find_active_users()
```

---

### 2. **Query Language**

**SQLAlchemy:**
- Pythonic expressions: `User.age >= 18`
- Type-safe (IDE autocomplete works)
- Closer to SQL

**Doctrine:**
- DQL (string-based): `"SELECT u FROM User u WHERE u.age >= 18"`
- Less type-safe (strings)
- QueryBuilder for fluent interface

---

### 3. **Migrations**

**SQLAlchemy:**
- Uses **Alembic** (separate tool)
```bash
alembic revision --autogenerate -m "Add users table"
alembic upgrade head
```

**Doctrine:**
- Built-in migrations
```bash
php bin/console doctrine:migrations:diff
php bin/console doctrine:migrations:migrate
```

---

### 4. **Configuration**

**SQLAlchemy:**
```python
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    pool_size=5,
    echo=True
)
SessionLocal = sessionmaker(bind=engine)
```

**Doctrine:**
```php
$config = ORMSetup::createAttributeMetadataConfiguration(
    paths: [__DIR__ . "/src/Entity"],
    isDevMode: true,
);

$connection = DriverManager::getConnection([
    'driver' => 'pdo_pgsql',
    'user' => 'user',
    'password' => 'pass',
    'dbname' => 'db',
]);

$entityManager = new EntityManager($connection, $config);
```

---

## Performance Comparison

| Feature | SQLAlchemy | Doctrine |
|---------|------------|----------|
| **Lazy Loading** | ✅ Fast | ✅ Fast |
| **Eager Loading** | ✅ `joinedload()` | ✅ `FETCH JOIN` |
| **Batch Processing** | ✅ Excellent | ✅ Good |
| **Connection Pooling** | ✅ Built-in | ⚠️ PHP-FPM handles |
| **Query Caching** | ✅ Manual | ✅ Built-in (2nd level) |

---

## Ecosystem & Framework Integration

### SQLAlchemy
- **Standalone:** Works independently
- **Flask:** Flask-SQLAlchemy (tight integration)
- **FastAPI:** Works natively
- **Django:** Separate (Django has its own ORM)

### Doctrine
- **Symfony:** Official ORM, deep integration
- **Laravel:** Not common (Eloquent is default)
- **Standalone:** Can be used independently

---

## Learning Curve

**SQLAlchemy:**
- ⭐⭐⭐⭐ (Medium-Hard)
- More flexible, more to learn
- Two layers: Core (SQL expressions) + ORM
- Documentation is comprehensive but dense

**Doctrine:**
- ⭐⭐⭐⭐ (Medium-Hard)
- Very similar to JPA/Hibernate (if you know Java)
- Repository pattern is intuitive
- Symfony integration makes it easier

---

## When to Choose Each?

### Choose **SQLAlchemy** if:
- ✅ You're building Python applications
- ✅ You want Pythonic query syntax
- ✅ You need maximum flexibility (Core + ORM)
- ✅ Working with Flask, FastAPI, or standalone
- ✅ You prefer explicit control

### Choose **Doctrine** if:
- ✅ You're building PHP applications
- ✅ You're using Symfony framework
- ✅ You come from JPA/Hibernate background
- ✅ You want built-in repositories
- ✅ You prefer convention over configuration

---

## Quick Reference: Common Operations

| Operation | SQLAlchemy | Doctrine |
|-----------|------------|----------|
| **Create session** | `get_session()` | `EntityManager::create()` |
| **Add entity** | `session.add(obj)` | `$em->persist($obj)` |
| **Save changes** | `session.commit()` | `$em->flush()` |
| **Rollback** | `session.rollback()` | Auto or `$em->rollback()` |
| **Find by ID** | `session.get(User, 1)` | `$em->find(User::class, 1)` |
| **Find all** | `session.query(User).all()` | `$repo->findAll()` |
| **Filter** | `.filter(User.age > 18)` | `->findBy(['age' => 18])` |
| **Delete** | `session.delete(obj)` | `$em->remove($obj)` |
| **Close** | `session.close()` | `$em->clear()` |

---

## Bottom Line

**SQLAlchemy and Doctrine are philosophical siblings:**
- Both implement Unit of Work + Identity Map
- Both are Data Mappers (not Active Record)
- Both separate domain logic from persistence
- Both are powerful, mature, and production-ready

**The main difference?** Language and ecosystem. If you understand one, you can easily learn the other! 🎯

---

## For Your Learning

Since you're learning SQLAlchemy, here's what transfers to Doctrine:
- ✅ Unit of Work pattern → Same concept
- ✅ Session → EntityManager (same role)
- ✅ `session.add()` → `persist()`
- ✅ `session.commit()` → `flush()`
- ✅ Identity Map → First-level cache
- ✅ Relationships → Same concepts (OneToMany, ManyToOne, etc.)

The patterns are identical, just the syntax differs! 🚀

