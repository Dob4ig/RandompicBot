import sqlite3


class UsersDB:
    """Класс  управления users.db
    #
    Столбцы:
    * user_id INT PRIMARY KEY
    * role TEXT DEFAULT user
    * channel INT DEFAULT NULL
    #
    #
    Варианты использования role:
    * user -- Обычный статус.
    * admin -- Администратор, расширенные права.
    * root -- Возможность напрямую изменять БД.
    * banned -- Заблокированный пользователь.
    #
    #
    __init__ -- Принимает путь к БД, если нет таблицы, создаёт её.
    add_user(id) -- Создаёт пользователя в БД (стандартная роль = user).
    set_admin(id) -- Меняет роль пользователя на admin.
    del_admin(id) -- Меняет роль пользователя на user.
    ban_user(id) -- Меняет роль пользователя на banned.
    add_channel(id, channel) -- Добавляет пользователю channel.
    del_channel(id, channel) -- Удаляет пользователю channel.
    get_users(*roles) -- Получаем set всех пользователей с ролью role.
    get_channel(id) -- Получаем id канала пользователя по его user_id.
    get_fullname(id) -- получаем никнейм пользователя по его user_id.
    """

    def __init__(self, path: str):
        self.path = path
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY,user_fullname TEXT, role TEXT DEFAULT 'user', channel INT DEFAULT NULL)")
        db.close()

    def add_user(self, id: int, name: str = None) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (id,))
        if cursor.fetchone():
            db.close()
            return "Вы уже зарегистрированы в боте, welcome"
        else:
            cursor.execute(
                "INSERT INTO users(user_id, user_fullname) VALUES(?,?)", (id, name))
            db.commit()
            db.close()
            return "Вы зарегистрировались, приятного пользования!"

    def set_admin(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (id,))
        if cursor.fetchone() == None:
            self.add_user(id)
        cursor.execute(
            "UPDATE users SET role = 'admin' WHERE user_id = ?", (id,))
        db.commit()
        db.close()
        return f"Пользователю {id} установлена роль admin!"

    def del_admin(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (id,))
        if cursor.fetchone() == None:
            self.add_user(id)
        cursor.execute(
            "UPDATE users SET role = 'user' WHERE user_id = ?", (id,))
        db.commit()
        db.close()
        return f"Пользователь {id} больше не admin!"

    def ban_user(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()

        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (id,))
        if cursor.fetchone() == None:
            self.add_user(id)
        cursor.execute(
            "UPDATE users SET role = 'banned' WHERE user_id = ?", (id,))
        db.commit()
        db.close()
        return f"Пользователь {id} заблокирован!"

    def unban_user(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ? AND role = 'banned'", (id,))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE users SET role = 'user' WHERE user_id = ?", (id,))
            db.commit()
            return f"Пользователь {id} разблокирован!"
        else:
            return f"Пользователь {id} не найден/не заблокирован!"

    def add_channel(self, id: int, channel: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (id,))
        if cursor.fetchone() == None:
            self.add_user(id)
        cursor.execute(
            "UPDATE users SET channel = ? WHERE user_id = ?", (channel, id))
        db.commit()
        db.close()
        return f"Пользователю {id} добавлен канал {channel}"

    def del_channel(self, id: int, channel: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute(
            "SELECT channel FROM users WHERE user_id = ? AND channel = ?", (id, channel))
        if cursor.fetchone():
            cursor.execute(
                "UPDATE users SET channel = NULL WHERE user_id = ? AND channel = ?", (id, channel))
            db.commit()
            db.close()
            return f"Пользователю {id} удалён канал {channel}"
        else:
            db.close()
            return "Пользователь/канал не найден"

    def get_users(self, *roles: str) -> set:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        users = set()
        for role in roles:
            cursor.execute(
                "SELECT user_id FROM users WHERE role = ? ", (role,))
            for turple in cursor.fetchall():
                users.add(turple[0])
        db.close()
        return users

    def get_channel(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute("SELECT channel FROM users WHERE user_id = ?", (id,))
        channel, = cursor.fetchone()  # int
        db.close()
        return str(channel)

    def get_fullname(self, id: int) -> str:
        db = sqlite3.connect(self.path)
        cursor = db.cursor()
        cursor.execute(
            "SELECT user_fullname FROM users WHERE user_id = ?", (id,))
        fullname, = cursor.fetchone()
        return fullname
