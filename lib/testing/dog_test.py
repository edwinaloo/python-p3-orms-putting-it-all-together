import dog


class TestDog:
    '''Class Dog in dog.py'''

    def test_has_name_and_breed_attributes(self):
        '''initializes with name and breed attributes.'''
        dog = dog.Dog(name="joey", breed="cocker spaniel")
        assert dog.name == "joey" and dog.breed == "cocker spaniel"

    def test_creates_table(self):
        '''contains method "create_table()" that creates table "dogs" if it does not exist.'''
        dog.CURSOR.execute("DROP TABLE IF EXISTS dogs")
        dog.Dog.create_table()
        assert dog.CURSOR.execute("SELECT * FROM dogs")

    def test_drops_table(self):
        '''contains method "drop_table()" that drops table "dogs" if it exists.'''
        sql = """
            CREATE TABLE IF NOT EXISTS dogs
                (id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT)
        """
        dog.CURSOR.execute(sql)
        dog.Dog.drop_table()

        sql_table_names = """
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """
        assert len(dog.CURSOR.execute(sql_table_names).fetchall()) == 0

    def test_saves_dog(self):
        '''contains method "save()" that saves a Dog instance to the database.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        joey = dog.Dog("joey", "cocker spaniel")
        joey.save()

        sql = """
            SELECT * FROM dogs
            WHERE name='joey'
            LIMIT 1
        """
        assert dog.CURSOR.execute(sql).fetchone() == (1, "joey", "cocker spaniel")

    def test_creates_dog(self):
        '''contains method "create()" that creates a new row in the database and returns a Dog instance.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        joey = dog.Dog.create("joey", "cocker spaniel")
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_creates_new_instance_from_db(self):
        '''contains method "new_from_db()" that takes a database row and creates a Dog instance.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES ('joey', 'cocker spaniel')
        """
        dog.CURSOR.execute(sql)
        sql = """
            SELECT * FROM dogs
            WHERE name='joey'
            LIMIT 1
        """
        row = dog.CURSOR.execute(sql).fetchone()
        joey = dog.Dog.new_from_db(row)
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_gets_all(self):
        '''contains method "get_all()" that returns a list of Dog instances for every record in the database.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        dog.Dog.create("joey", "cocker spaniel")
        dog.Dog.create("fanny", "cockapoo")

        dogs = dog.Dog.get_all()
        assert (
            (dogs[0].id, dogs[0].name, dogs[0].breed)
            == (1, "joey", "cocker spaniel")
            and (dogs[1].id, dogs[1].name, dogs[1].breed)
            == (2, "fanny", "cockapoo")
        )

    def test_finds_by_name(self):
        '''contains method "find_by_name()" that returns a Dog instance corresponding to its database record retrieved by name.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        dog.Dog.create("joey", "cocker spaniel")

        joey = dog.Dog.find_by_name("joey")
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_finds_by_id(self):
        '''contains method "find_by_id()" that returns a Dog instance corresponding to its database record retrieved by id.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        dog.Dog.create("joey", "cocker spaniel")

        joey = dog.Dog.find_by_id(1)
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_finds_by_name_and_breed(self):
        '''contains method "find_or_create_by()" that takes a name and a breed as arguments and returns a Dog instance matching that record.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        dog.Dog.create("joey", "cocker spaniel")

        joey = dog.Dog.find_or_create_by("joey", "cocker spaniel")
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_finds_by_name_and_breed(self):
        '''contains method "find_or_create_by()" that takes a name and a breed as arguments and creates a Dog instance matching that record if it does not exist.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()

        joey = dog.Dog.find_or_create_by("joey", "cocker spaniel")
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_saves_with_id(self):
        '''contains a method "save()" that saves a Dog instance to the database and returns a Dog instance with id.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        joey = dog.Dog("joey", "cocker spaniel")
        joey.save()
        assert (joey.id, joey.name, joey.breed) == (1, "joey", "cocker spaniel")

    def test_updates_record(self):
        '''contains a method "update()" that updates an instance's corresponding database record to match its new attribute values.'''
        dog.Dog.drop_table()
        dog.Dog.create_table()
        joey = dog.Dog.create("joey", "cocker spaniel")
        joey.name = "joseph"
        joey.update()

        assert dog.Dog.find_by_id(1).name == "joseph" and dog.Dog.find_by_name("joey") is None
