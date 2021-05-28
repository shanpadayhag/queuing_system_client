import mysql.connector

def createDB():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='root'
    )
    csr = conn.cursor()

    sqlStatement = "CREATE SCHEMA IF NOT EXISTS `cc15`"
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
        CREATE TABLE IF NOT EXISTS `number` (
            `cs` int NOT NULL,
            `emc` int NOT NULL,
            `is` int NOT NULL,
            `it` int NOT NULL,
            PRIMARY KEY (`cs`,`emc`,`is`,`it`)
        );

        CREATE TABLE IF NOT EXISTS `course` (
            `id` int NOT NULL AUTO_INCREMENT,
            `name` varchar(255) NOT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE IF NOT EXISTS `enrollment` (
            `id` int NOT NULL AUTO_INCREMENT,
            `queue` varchar(255) NOT NULL,
            `name` varchar(255) NOT NULL,
            `course` int NOT NULL,
            `enrolled_at` datetime NOT NULL,
            PRIMARY KEY (`id`),
            KEY `enrollment_course_idx` (`course`),
            CONSTRAINT `enrollment_course` FOREIGN KEY (`course`) REFERENCES `course` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
        );

        CREATE TABLE IF NOT EXISTS `year_level` (
            `id` int NOT NULL AUTO_INCREMENT,
            `year` varchar(255) DEFAULT NULL,
            PRIMARY KEY (`id`)
        );

        CREATE TABLE IF NOT EXISTS `user` (
            `id` int NOT NULL AUTO_INCREMENT,
            `first_name` varchar(255) NOT NULL,
            `last_name` varchar(255) NOT NULL,
            `school_id` varchar(255) NOT NULL,
            `password` varchar(255) NOT NULL,
            `type` tinyint(1) NOT NULL,
            PRIMARY KEY (`id`),
            KEY `type` (`type`)
        );

        CREATE TABLE IF NOT EXISTS `user_student` (
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

        CREATE TABLE IF NOT EXISTS `appointment` (
            `id` int NOT NULL AUTO_INCREMENT,
            `student` int NOT NULL,
            `teacher` int NOT NULL,
            `reason` varchar(255) NOT NULL,
            `datetime` datetime NOT NULL,
            `status` int NOT NULL DEFAULT '0',
            PRIMARY KEY (`id`),
            KEY `appointment_student_idx` (`student`),
            KEY `appointment_teacher_idx` (`teacher`),
            CONSTRAINT `appointment_student` FOREIGN KEY (`student`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT `appointment_teacher` FOREIGN KEY (`teacher`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
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
        DELETE FROM `number`;
        DELETE FROM `course`;
        DELETE FROM `enrollment`;
        DELETE FROM `year_level`;
        DELETE FROM `user`;
        DELETE FROM `user_student`;
        DELETE FROM `appointment`;

        INSERT INTO `course` (`name`) VALUES ('Computer Science');
        INSERT INTO `course` (`name`) VALUES ('Entertainment and Multimedia Computing');
        INSERT INTO `course` (`name`) VALUES ('Information System');
        INSERT INTO `course` (`name`) VALUES ('Information Technology');
        
        INSERT INTO `year_level` (`year`) VALUES ('First Year');
        INSERT INTO `year_level` (`year`) VALUES ('Second Year');
        INSERT INTO `year_level` (`year`) VALUES ('Third Year');
        INSERT INTO `year_level` (`year`) VALUES ('Fourth Year');

        INSERT INTO `number` (`cs`, `emc`, `is`, `it`) VALUES ('0', '0', '0', '0');
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