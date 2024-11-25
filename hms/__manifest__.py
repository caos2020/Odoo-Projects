

{
    "name" : "Hospital Addons",
     "description" : "Hospital App",
    "author" : "Mohamed Ali Moawad",
    "data": ['reports/hms_patient_template.xml',
             'reports/hms_patient_report.xml' ,
              'security/hms_security.xml',
             'security/ir.model.access.csv',
             'views/hospiatal_patient_view.xml',
             'views/hospital_dept_view.xml','views/hospital_doc_view.xml','views/hospital_loghistory.xml'
    ] ,
    'installable': True,
    'application': True,
    "sequence" :  -1,
    "depends" : ['base'],
}