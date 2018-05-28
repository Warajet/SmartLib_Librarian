class Book:
    def __init__(self, book_id, title, isbn, added_on, author, publisher, rfid =  None):
        self.book_id = book_id
        self.title = title
        self.isbn = isbn
        self.added_on = added_on
        self.author = author
        self.publisher = publisher
        self.rfid = rfid

    def __str__(self):
        return self.title

    # Compare method for book (Compare by ID)
    def __eq__(self, other):
        if other == None:
            return False
        return self.book_id == other.book_id