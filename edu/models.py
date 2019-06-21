from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(u'名称', max_length=50)
    address = models.CharField(u'地址', max_length=100)
    begin_date = models.DateField(u'开始日期', blank=False, null=False)
    end_date = models.DateField(u'结束日期', blank=False, null=False )
    pub_date = models.DateTimeField(u'添加日期', auto_now_add=True)

    class Meta:
        verbose_name = '期次'
        verbose_name_plural = '期次'

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(u'名称', max_length=50,primary_key=True)
    pub_date = models.DateTimeField(u'添加日期', auto_now_add=True)

    class Meta:
        verbose_name = '地市'
        verbose_name_plural = '地市'

    def __str__(self):
        return self.name

class Org(models.Model):
    name = models.CharField(u'名称', max_length=50,primary_key=True)
    city = models.ForeignKey(City, related_name='org_of_city', verbose_name=u'所属地市', blank=False, null=False)
    pub_date = models.DateTimeField(u'添加日期', auto_now_add=True)

    class Meta:
        verbose_name = '法人'
        verbose_name_plural = '法人'

    def __str__(self):
        return self.name

CLASS_TYPE = (
    (u'晨曦', u'晨曦'),
    (u'晨光', u'晨光'),
    (u'曙光', u'曙光'),
    (u'朝阳', u'朝阳'),
    (u'旭日', u'旭日'),
)

class Import_Summary(models.Model):
    education = models.ForeignKey(School,related_name='edu_of_import', verbose_name=u'期次', blank=False, null=False)
    data_count = models.IntegerField(u'条数', default=0)
    remarks = models.CharField(u'备注', max_length=255)
    is_saved = models.BooleanField(u'保存', default=False)
    search_date = models.DateField(u'添加日期', auto_now_add=True)
    pub_date = models.DateTimeField(u'添加时间', auto_now_add=True)


class Student(models.Model):
    SEX_TYPE = (
        (u'男', u'男'),
        (u'女', u'女'),
    )
    name = models.CharField(u'姓名', max_length=50, blank=False, null=False)
    sex = models.CharField(
        u'性别', max_length=50,
        choices=SEX_TYPE,
        default=u'男',
    )
    company = models.CharField(u'单位', max_length=50)
    nation = models.CharField(u'民族', max_length=50)
    birth = models.CharField(u'生日', max_length=50)
    party = models.CharField(u'组织关系', max_length=50)
    job = models.CharField(u'职务', max_length=50)
    phone = models.CharField(u'电话', max_length=50)
    remarks = models.CharField(u'备注', max_length=50)
    org = models.ForeignKey(Org, related_name='student_of_org', verbose_name=u'法人', blank=True, null=True)
    school = models.ForeignKey(School,related_name='stu_of_school', verbose_name=u'期次', blank=True, null=True)
    inport_info = models.ForeignKey(Import_Summary, related_name='t_import', verbose_name=u'导入', blank=True, null=True,on_delete=models.CASCADE,)
    pub_date = models.DateTimeField(u'添加日期', auto_now_add=True)
    class Meta:
        verbose_name = '学员'
        verbose_name_plural = '学员'

    def __str__(self):
        return self.name
class Classes(models.Model):  # 这就是具体的中间表模型
    student = models.ForeignKey(Student,related_name='student_of_class', verbose_name=u'学员', blank=False, null=False, on_delete=models.CASCADE)
    education = models.ForeignKey(School,related_name='edu_of_class', verbose_name=u'期次', blank=False, null=False)
    theclass = models.CharField(
        u'班级', max_length=50,
        choices=CLASS_TYPE,
        default=u'晨曦',
    )
    master = models.CharField(u'班主任', max_length=50)
    class Meta:
        verbose_name = '分班'
        verbose_name_plural = '分班'

    def __str__(self):
        return self.name

