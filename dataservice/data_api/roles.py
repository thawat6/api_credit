from rolepermissions.roles import AbstractUserRole


class TripManager(AbstractUserRole):
    available_permissions = {
        'view_trip_manager': True,
    }


class SalePerson(AbstractUserRole):
    available_permissions = {
        'view_sale_person': True,
    }


class BackOfficer(AbstractUserRole):
    available_permissions = {
        'view_back_office': True,
    }


class OrderManager(AbstractUserRole):
    available_permissions = {
        'view_order_manager': True,
    }


class ServiceAdmin(AbstractUserRole):
    available_permissions = {
        'view_service_admin': True,
    }


class Driver(AbstractUserRole):
    available_permissions = {
        'view_driver': True,
    }
