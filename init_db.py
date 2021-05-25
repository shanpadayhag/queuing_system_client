import mysql.connector

def createDB():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root'
    )
    csr = conn.cursor()

    sqlStatement = "CREATE SCHEMA `cc15`"
    csr.execute(sqlStatement)

    csr.close()
    conn.close()
        
def createTables():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='cc15'
    )
    csr = conn.cursor()

    sqlStatement = """
        CREATE TABLE `course` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) NOT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE `year_level` (
            `id` int NOT NULL AUTO_INCREMENT,
            `year` varchar(255) DEFAULT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE `user` (
            `id` int NOT NULL AUTO_INCREMENT,
            `first_name` varchar(255) NOT NULL,
            `last_name` varchar(255) NOT NULL,
            `school_id` varchar(255) NOT NULL,
            `password` varchar(255) NOT NULL,
            `type` tinyint(1) NOT NULL,
            PRIMARY KEY (`id`),
            KEY `type` (`type`)
        );

        CREATE TABLE `user_student` (
            `id` int NOT NULL,
            `course` int NOT NULL,
            `year` int NOT NULL,
            PRIMARY KEY (`id`,`course`,`year`),
            KEY `student_course_idx` (`course`),
            KEY `student_year_idx` (`year`),
            CONSTRAINT `student_course` FOREIGN KEY (`course`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `student_user` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `student_year` FOREIGN KEY (`year`) REFERENCES `year_level` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
        );
    """
    for statement in sqlStatement.split(';'):
        if statement.strip() != '':
             csr.execute(statement + ';')
    conn.commit()

    csr.close()
    conn.close()
        
def addData():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root',
        database='cc15'
    )
    csr = conn.cursor()

    sqlStatement = """
        INSERT INTO `course` (`name`) VALUES ('');
        INSERT INTO `course` (`name`) VALUES ('Computer Science');
        INSERT INTO `course` (`name`) VALUES ('Entertainment and Multimedia Computing');
        INSERT INTO `course` (`name`) VALUES ('Information System');
        INSERT INTO `course` (`name`) VALUES ('Information Technology');
        
        INSERT INTO `year_level` (`year`) VALUES ('');
        INSERT INTO `year_level` (`year`) VALUES ('First Year');
        INSERT INTO `year_level` (`year`) VALUES ('Second Year');
        INSERT INTO `year_level` (`year`) VALUES ('Third Year');
        INSERT INTO `year_level` (`year`) VALUES ('Fourth Year');
    """
    for statement in sqlStatement.split(';'):
        if statement.strip() != '':
             csr.execute(statement + ';')
    conn.commit()

    csr.close()
    conn.close()

createDB()
createTables()
addData()