from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from booking.models import RoomCategory, Room
from restaurant.models import MenuCategory, FoodItem, Table
from facilities.models import Facility
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Create sample dummy data for StaySphere'

    def download_image(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return SimpleUploadedFile(
                    name=url.split('/')[-1],
                    content=response.content,
                    content_type='image/jpeg'
                )
        except:
            pass
        return None

    def handle(self, *args, **options):
        self.stdout.write('Creating sample dummy data...')

        # Create room categories
        categories_data = [
            {
                'name': 'Single Room',
                'description': 'Comfortable single room with modern amenities',
                'base_price': Decimal('2000.00'),
                'max_occupancy': 1,
                'image_url': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800'
            },
            {
                'name': 'Double Room',
                'description': 'Spacious double room perfect for couples',
                'base_price': Decimal('3000.00'),
                'max_occupancy': 2,
                'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'
            },
            {
                'name': 'Deluxe Room',
                'description': 'Luxurious deluxe room with premium features',
                'base_price': Decimal('5000.00'),
                'max_occupancy': 2,
                'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'
            },
            {
                'name': 'Suite',
                'description': 'Executive suite with separate living area',
                'base_price': Decimal('8000.00'),
                'max_occupancy': 4,
                'image_url': 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800'
            }
        ]

        for cat_data in categories_data:
            image_url = cat_data.pop('image_url', None)
            category, created = RoomCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                if image_url:
                    image = self.download_image(image_url)
                    if image:
                        category.image = image
                        category.save()
                self.stdout.write(f'Created room category: {category.name}')
            else:
                # Update existing category with image if missing
                if image_url and not category.image:
                    image = self.download_image(image_url)
                    if image:
                        category.image = image
                        category.save()
                        self.stdout.write(f'Updated room category with image: {category.name}')

        # Create rooms
        rooms_data = [
            {'room_number': '101', 'category': 'Single Room', 'floor': 1, 'image_url': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800'},
            {'room_number': '102', 'category': 'Single Room', 'floor': 1, 'image_url': 'https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800'},
            {'room_number': '201', 'category': 'Double Room', 'floor': 2, 'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'},
            {'room_number': '202', 'category': 'Double Room', 'floor': 2, 'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800'},
            {'room_number': '301', 'category': 'Deluxe Room', 'floor': 3, 'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'},
            {'room_number': '302', 'category': 'Deluxe Room', 'floor': 3, 'image_url': 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800'},
            {'room_number': '401', 'category': 'Suite', 'floor': 4, 'image_url': 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800'},
            {'room_number': '402', 'category': 'Suite', 'floor': 4, 'image_url': 'https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=800'},
        ]

        for room_data in rooms_data:
            image_url = room_data.pop('image_url', None)
            category = RoomCategory.objects.get(name=room_data['category'])
            room, created = Room.objects.get_or_create(
                room_number=room_data['room_number'],
                defaults={
                    'category': category,
                    'floor': room_data['floor']
                }
            )
            if created:
                if image_url:
                    image = self.download_image(image_url)
                    if image:
                        room.image = image
                        room.save()
                self.stdout.write(f'Created room: {room.room_number}')
            else:
                # Update existing room with image if missing
                if image_url and not room.image:
                    image = self.download_image(image_url)
                    if image:
                        room.image = image
                        room.save()
                        self.stdout.write(f'Updated room with image: {room.room_number}')

        # Create menu categories
        menu_categories_data = [
            {'name': 'Starters', 'description': 'Appetizers and starters'},
            {'name': 'Main Course', 'description': 'Main dishes and entrees'},
            {'name': 'Desserts', 'description': 'Sweet endings'},
            {'name': 'Beverages', 'description': 'Drinks and beverages'},
        ]

        for cat_data in menu_categories_data:
            category, created = MenuCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created menu category: {category.name}')

        # Create food items
        food_items_data = [
            {
                'name': 'Paneer Tikka',
                'category': 'Starters',
                'description': 'Grilled cottage cheese with spices',
                'price': Decimal('250.00'),
                'food_type': 'veg',
                'preparation_time': 20,
                'image_url': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800'
            },
            {
                'name': 'Chicken Tikka',
                'category': 'Starters',
                'description': 'Grilled chicken with spices',
                'price': Decimal('350.00'),
                'food_type': 'non_veg',
                'preparation_time': 25,
                'image_url': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=800'
            },
            {
                'name': 'Butter Chicken',
                'category': 'Main Course',
                'description': 'Creamy chicken curry with butter',
                'price': Decimal('450.00'),
                'food_type': 'non_veg',
                'preparation_time': 30,
                'image_url': 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=800'
            },
            {
                'name': 'Paneer Butter Masala',
                'category': 'Main Course',
                'description': 'Creamy cottage cheese curry',
                'price': Decimal('380.00'),
                'food_type': 'veg',
                'preparation_time': 25,
                'image_url': 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=800'
            },
            {
                'name': 'Gulab Jamun',
                'category': 'Desserts',
                'description': 'Sweet milk dumplings in sugar syrup',
                'price': Decimal('120.00'),
                'food_type': 'veg',
                'preparation_time': 5,
                'image_url': 'https://images.unsplash.com/photo-1666190054763-1b8493de2e8c?w=800'
            },
            {
                'name': 'Fresh Lime Soda',
                'category': 'Beverages',
                'description': 'Refreshing lime soda',
                'price': Decimal('80.00'),
                'food_type': 'veg',
                'preparation_time': 5,
                'image_url': 'https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=800'
            },
        ]

        for item_data in food_items_data:
            image_url = item_data.pop('image_url', None)
            category = MenuCategory.objects.get(name=item_data['category'])
            food_item, created = FoodItem.objects.get_or_create(
                name=item_data['name'],
                defaults={
                    'category': category,
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'food_type': item_data['food_type'],
                    'preparation_time': item_data['preparation_time']
                }
            )
            if created:
                if image_url:
                    image = self.download_image(image_url)
                    if image:
                        food_item.image = image
                        food_item.save()
                self.stdout.write(f'Created food item: {food_item.name}')
            else:
                # Update existing food item with image if missing
                if image_url and not food_item.image:
                    image = self.download_image(image_url)
                    if image:
                        food_item.image = image
                        food_item.save()
                        self.stdout.write(f'Updated food item with image: {food_item.name}')

        # Create tables
        tables_data = [
            {'table_number': 'T1', 'capacity': 2, 'location': 'Ground Floor'},
            {'table_number': 'T2', 'capacity': 2, 'location': 'Ground Floor'},
            {'table_number': 'T3', 'capacity': 4, 'location': 'Ground Floor'},
            {'table_number': 'T4', 'capacity': 4, 'location': 'First Floor'},
            {'table_number': 'T5', 'capacity': 6, 'location': 'First Floor'},
            {'table_number': 'T6', 'capacity': 8, 'location': 'Terrace'},
        ]

        for table_data in tables_data:
            table, created = Table.objects.get_or_create(
                table_number=table_data['table_number'],
                defaults=table_data
            )
            if created:
                self.stdout.write(f'Created table: {table.table_number}')

        # Create facilities
        facilities_data = [
            {
                'name': 'Swimming Pool',
                'facility_type': 'swimming_pool',
                'description': 'Olympic size swimming pool with clean water',
                'capacity': 50,
                'hourly_rate': Decimal('200.00'),
                'operating_hours_start': '06:00:00',
                'operating_hours_end': '22:00:00',
                'image_url': 'https://images.unsplash.com/photo-1576013551627-0cc20b96c2a7?w=800'
            },
            {
                'name': 'Fitness Center',
                'facility_type': 'gym',
                'description': 'Modern gym with latest equipment',
                'capacity': 30,
                'hourly_rate': Decimal('150.00'),
                'operating_hours_start': '05:00:00',
                'operating_hours_end': '23:00:00',
                'image_url': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800'
            },
            {
                'name': 'Spa & Wellness',
                'facility_type': 'spa',
                'description': 'Relaxing spa treatments and massages',
                'capacity': 10,
                'hourly_rate': Decimal('500.00'),
                'operating_hours_start': '09:00:00',
                'operating_hours_end': '20:00:00',
                'image_url': 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=800'
            },
            {
                'name': 'Gaming Zone',
                'facility_type': 'gaming_zone',
                'description': 'Entertainment zone with games and activities',
                'capacity': 20,
                'hourly_rate': Decimal('100.00'),
                'operating_hours_start': '10:00:00',
                'operating_hours_end': '23:00:00',
                'image_url': 'https://images.unsplash.com/photo-1511882150382-421056c89033?w=800'
            },
        ]

        for facility_data in facilities_data:
            image_url = facility_data.pop('image_url', None)
            facility, created = Facility.objects.get_or_create(
                name=facility_data['name'],
                defaults=facility_data
            )
            if created:
                if image_url:
                    image = self.download_image(image_url)
                    if image:
                        facility.image = image
                        facility.save()
                self.stdout.write(f'Created facility: {facility.name}')
            else:
                # Update existing facility with image if missing
                if image_url and not facility.image:
                    image = self.download_image(image_url)
                    if image:
                        facility.image = image
                        facility.save()
                        self.stdout.write(f'Updated facility with image: {facility.name}')

        self.stdout.write(self.style.SUCCESS('Sample dummy data created successfully!'))
