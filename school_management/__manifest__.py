
{
    'name' : 'School Management',
    'version' : '1.0',
    'summary': 'School Management System',
    'sequence': -100,
    'description': """School Management System""",
    'category': 'Productivity',
    'website': 'https://www.odooappliance.com',
    'images' : [],
    'depends' : [
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/cron.xml',
        'views/student.xml',
        'views/marksheet.xml',
        'views/student_class.xml',
        'views/teachers.xml',
        'views/activities.xml',
        'views/timetable.xml',
        'views/timeslot.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
