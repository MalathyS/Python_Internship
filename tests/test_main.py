from fastapi.testclient import TestClient
import pytest

from main import app
from dependencies import get_employee_service
from tests.test_employee_repository import test_update_employee


client = TestClient(app)

class FakeEmployeeService:
    @pytest.mark.asyncio
    async def get_employees(self):
        return [
            {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "designation": "Developer",
                "salary": 60000.0,
                "department_id": 1
            }
        ]
    @pytest.mark.asyncio
    async def get_employee_by_id(self, employee_id: int):
        if employee_id == 1:
            return {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com",
                "designation": "Developer",
                "salary": 60000.0,
                "department_id": 1
            }
        return None
    @pytest.mark.asyncio
    async def add_employee(self, employee):
        return {
            "id": 2,
            "name": employee.name,
            "email": employee.email,
            "designation": employee.designation,
            "salary": employee.salary,
            "department_id": employee.department_id
        }
    @pytest.mark.asyncio
    async def update_employee(self, employee_id: int, updated_employee):
        if employee_id == 1:
            return {
                "id": 1,
                "name": updated_employee.name,
                "email": updated_employee.email,
                "designation": updated_employee.designation,
                "salary": updated_employee.salary,
                "department_id": updated_employee.department_id
            }
        return None
    @pytest.mark.asyncio
    async def delete_employee(self, employee_id: int):
        if employee_id == 1:
            return {"message": "Employee deleted successfully"}
        return None

@pytest.mark.asyncio
async def test_get_employees(authenticated_client):
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        response = authenticated_client.get("/employees/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["name"] == "John Doe"
    finally:
        app.dependency_overrides.clear()
@pytest.mark.asyncio
async def test_get_employee_by_id(authenticated_client):
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        response = authenticated_client.get("/employees/1")

        assert response.status_code == 200
        assert response.json()["name"] == "John Doe"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_get_employee_by_id_not_found(authenticated_client):
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        response = authenticated_client.get("/employees/999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Employee not found"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_add_employee(authenticated_client):
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        new_employee = {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "designation": "Product Manager",
            "salary": 80000.0
        }
        response = authenticated_client.post("/employees/add", json=new_employee)

        assert response.status_code == 200
        assert response.json()["name"] == "Alice Johnson"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_update_employee():
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        updated_employee = {
            "name": "John Doe Updated",
            "email": "john.updated@example.com",
            "designation": "Senior Developer",
            "salary": 70000.0
        }
        response = client.put("/employees/update/1", json=updated_employee)

        assert response.status_code == 200
        assert response.json()["name"] == "John Doe Updated"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_update_employee_not_found():
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        updated_employee = {
            "name": "Non-existent Employee",
            "email": "nonexistence@example.com",
            "designation": "Manager",
            "salary": 70000.0
        }
        response = client.put("/employees/update/999", json=updated_employee)

        assert response.status_code == 404
        assert response.json()["detail"] == "Employee not found"
    finally:
        app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_delete_employee():
    app.dependency_overrides[get_employee_service] = (
        lambda: FakeEmployeeService()
    )
    try:
        response = client.delete("/employees/delete/1")

        assert response.status_code == 200
        assert response.json()["message"] == "Employee deleted successfully"
    finally:
        app.dependency_overrides.clear()