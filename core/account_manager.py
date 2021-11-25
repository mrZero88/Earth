from models.account import Account


class AccountManager:
    accounts = []

    def __init__(self, conn):
        self.conn = conn

    def load_accounts(self):
        if self.exists_accounts():
            self.load_accounts_from_database()

    def exists_accounts(self):
        cur = self.conn.cursor()
        row = cur.execute("select * from accounts").fetchone()
        return True if row else False

    def insert_account_in_database(self, account):
        cur = self.conn.cursor()
        cur.execute(
            "insert into accounts "
            "("
            "name,"
            "email,"
            "user_name,"
            "password,"
            "provider,"
            "imap,"
            "created_at,"
            "is_default"
            ")"
            " values "
            "(?,?,?,?,?,?,?,?)'", (
                account.name,
                account.email,
                account.user_name,
                account.password,
                account.provider,
                account.imap,
                account.created_at,
                account.is_default))
        self.conn.commit()

    def load_accounts_from_database(self):
        cur = self.conn.cursor()
        for row in cur.execute("select * from accounts"):
            self.accounts.append(Account(
                id=row[0],
                name=row[1],
                email=row[2],
                user_name=row[3],
                password=row[4],
                provider=row[5],
                imap=row[6],
                created_at=row[7],
                is_default=row[8] == 1
            ))

    def add_account(self, account):
        self.accounts.append(account)
        self.insert_account_in_database(account)

    def get_default_account(self):
        return next(filter(lambda account: account.is_default is True, self.accounts), None)

    def get_accounts(self):
        return self.accounts
