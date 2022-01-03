from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

# อ่านรายละเอียดได้ที่ https://www.django-rest-framework.org/api-guide/pagination/#pagenumberpagination

class WatchListPagination(PageNumberPagination):
    # จำนวนหน้าสูงสุดที่จะแสดงผลได้
    page_size = 7
    # ตั้งชื้อสำหรับการใช้ parameter ในการแสดงผลถ้าไม่มีการตั้งจะแสดงเป็น ?page=<เลขหน้า>
    page_query_param = 'p'
    # ใช้สำหรับตั้งค่าจำนวนของการแสดงผลในแต่ละหน้า โดยการใช้ parameter ที่ตั้งขึ้น [ในนี้ตั้งว่า size] แล้วสามารถใช้ในการกำหนดจำนวนข้อมูลแต่ละหน้าได้เลย
    page_size_query_param = 'size'
    # ใช้สำหรับจำกัดจำนวนข้อมูลในแต่ละหน้า จากการกำหนดจำนวนของข้อมูลในแต่ละหน้าโดยใช้ parameter size เพื่อป้องกันการป้อนจำนวนที่สูงเกินไป
    # สามารถใช้ max_page_size ในการกำหนดข้อมูลสูงสุดได้ต่อให้ใส่เลขสูงกว่าเลขที่ตั้งไว้ใน max_page_size ก็จะแสดงได้สูงสุดแค่เลขที่ตั้งไว้
    max_page_size = 10
    # ใช้ตั้งค่าข้อความในการเรียกดูหน้าสุดท้าย
    last_page_strings = 'end'

# LimitOffsetPagination ใช้ปรับจำนวนข้อมูลที่จะแสดงและปรับ offset สำหรับแสดงหน้าถัดไปด้วย
class WatchListLimitOffsetPagination(LimitOffsetPagination):
    # ใช้าสำหรับตั้งจำนวนที่ต้องการให้แสดงผลต่อ 1 หน้าว่าจะแสดงผลจำนวนข้อมูลออกมาเท่าไหร่
    default_limit = 5
    # ตั้งค่า limit สูงสุดที่จะแสดงผลออกมา ถ้าใส่เกินเลขที่กำหนดก็จะแสดงได้สูงสุดแค่ที่กำหนดไว้
    max_limit = 10
    # ใช้สำหรับตั้งค่า parameter ในการเรียกใช้การ limit [ จำกัดจำนวน ]
    limit_query_param = 'limit'
    # ใชำสำหรับตั้งค่า parameter ในการเรียกใช้ตัวเริ่มต้นสำหรับการ filter ข้อมูลมาแสดงผล
    offset_query_param = 'start'
    