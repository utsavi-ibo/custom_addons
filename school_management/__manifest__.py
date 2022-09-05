
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
        'mail',
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/cron.xml',
        'data/student_sequence.xml',
        'wizard/remark_wizard.xml',
        'views/student.xml',
        'views/marksheet.xml',
        'views/pass_students.xml',
        'views/student_class.xml',
        'views/teachers.xml',
        'views/activities.xml',
        'views/timetable.xml',
        'views/timeslot.xml',
        'views/sale_inherit.xml',
        'views/purchase.xml',
        'report/report_card.xml',
        'report/purchase_order_inherit.xml'],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,

}
