from rest_framework import serializers, validators
from watchlist_app.models import *

#################### serializers.ModelSerializer ####################

class ReviewSerializer(serializers.ModelSerializer):
    reviews_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        exclude = ['watchlist',]
        # fields = "__all__"

class WatchListSerializer(serializers.ModelSerializer):
    
    ''' len_name เป็นตัวแปรที่ประกาศไว้เพื่อจะดำเนินการอะไรบางอย่างกับข้อมูลที่อยู่ใน model ของเรา '''
    # len_name = serializers.SerializerMethodField()
    
    # Show rating point of movie"
    # reviews = ReviewSerializer(many = True, read_only = True)
    
    # serializers.Charfield() สามารถใช้ในการแสดงผลข้อมูลถูก ForeignKey มา สามารถเลือกได้ว่าจะคืนค่าตัวใดบ้าง เช่น platform.name ก็คือแสดงผล name
    # ที่ถูกผูกเข้ากับ platform นั้นเลย
    platform = serializers.CharField(source = 'platform.name')
    
    class Meta:
        model = WatchList
        fields = "__all__"
        # fields = ['id', 'name', 'description']
        ''' exclude สามารถใช้ปิดตัวที่ไม่ต้องการแสดงผลได้ ถ้า fields จะเป็นการเลือกตัวที่ต้องการแสดงผล '''
        # exclude = ['active']
        
    # ''' object คือ ข้อมูลที่เราจัดเก็บใน model นั้น ๆ เช่น ID, ชื่อ หรืออะไรก็ตามที่เราบันทึกลงใน Model 
    # โดยเราสามารถเข้าถึง column ใน model ได้โดยการใช้ object.< columnname > เพื่อดำเนินการบางอย่างกับข้อมูลใน Column นั้น ๆ
    # จาก def ชุดถัดไปจะเห็นว่ามีการใช้ len ในการนับจำนวนตัวอักษรใน column ที่ชื่อว่า name ใน model ของเรา < Model คือ Movie > '''
    
    # def get_len_name(self, object):
    #     return  len(object.name)

    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Name and Description should be different!")
    #     else:
    #         return data
        
    # def validate_name(self, value):
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name is too short!")
    #     else:
    #         return value
    
    
# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     ''' ตัวแปรที่ชื่อ watchlist ต้องตั้งให้ตรงกับ related_name ใน models.py ถ้าไม่ตรงกันข้อมูลจะไม่ถูกแสดงผล [ Nested Relationship ] 
#     Nested Relationship นั้นใช้ในการแสดงผลข้อมูลในลักษณะซ้อนทับกัน ตัวอย่างแบบโค๊ดนี้ watchlist 1 รายการถูกฉายบน Platform เพียง 1
#     แต่ Platform 1 Platform สามารถฉาย Watchlist ได้มากกว่า 1 รายการแน่ ๆ '''
    
#     # watchlist = WatchListSerializer(many = True, read_only = True)
    
#     ''' StringRelatedField จะใช้เมื่อต้องการแสดงเฉพาะค่าใดค่าหนึ่งโดยสามารถเลือกได้ว่าจะแสดงค่าไหนซึ่งค่าที่จะแสดงผลนั้นจะต้องอยู่ใน type string เสมอ
#     ซึ่งค่าที่ต้องการนำไปแสดงผลนั้นให้ดูไปที่ Model ของ Serializer ตัวนั้น ๆ ใช้งานอย่างโค๊ดนี้ให้ไปดูที่ Class Watchlist ในไฟล์ models.py 
#     ตรงส่วงที่เป็น def __str__(self): จะมีการ return ตัวแปรที่ต้องการออกมาในรูปแบบของ String'''
    
#     watchlist = serializers.StringRelatedField(many = True, read_only = True)
    
#     ''' PrimaryKeyRelatedField ใช้สำหรับแสดงผลเฉพาะ field ที่เป็น PrimaryKey ที่เรากำหนดไว้ตอนสร้าง model นั่นเอง ส่วนใหญ่มักจะเป็น ID [ลำดับที่ของข้อมูล]'''
#     # watchlist = serializers.PrimaryKeyRelatedField(many = True, read_only = True)
    
#     ''' hyperlinkedRelatedField ใช้สำหรับแสดง link ที่สามารถใช้งานได้ใน serializer ตัวนั้น ๆ ทั้งหมดโดยต้องเข้าไปเพิ่ม context={'request': request}
#     ใน views.py ในส่วนของ GET Method ด้วยถ้าไม่งั้นมันจะไม่ทำงาน '''
#     # watchlist = serializers.HyperlinkedRelatedField(
#     #     many = True, 
#     #     read_only = True, 
#     #     view_name = 'movie-detail'
#     # )
    
#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"

''' HyperlinkedModelSerializer เอาไว้ใช้สำหรับการแสดง Link ที่ใช้สำหรับเชื่อมต่อไปยังหน้าอื่น ๆ หรือ API อื่น ๆ ตามที่ออกแบบไว้ '''
class StreamPlatformSerializer(serializers.ModelSerializer):
    
    watchlist = WatchListSerializer(many = True, read_only = True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        
        
#################### serializers.ModelSerializer ####################



#################### serializers.Serializer ####################

# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
    
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     # validate by validators
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     # instance is old value and validated_data is new value
#     def update(sellf, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#     ''' Validate เป็นการตรวจสอบความถูกต้องของข้อมูลที่ทำการรับมาว่าเป็นไปตามที่ต้องการไหม ถ้าไม่ใช่ก็คืนค่า Error ไปแจ้ง User ต่อไป '''
#     # validete field-level
#     # value is particular of name in model name is Movie
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value
    
#     # validate object-level
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Name and Description should be different!")
#         else:
#             return data

#################### serializers.Serializer ####################