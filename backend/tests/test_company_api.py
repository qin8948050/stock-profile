import pytest
import requests
from core.config import config

BASE_URL = f"http://{config.server.host}:{config.app.port}{config.api.prefix}"

def test_create_company():
    data = {
        "name": "Test Company",
        "ticker": "TEST",
        "main_business": "Test Business",
        "employee_count": 100
    }
    response = requests.post(f"{BASE_URL}/companies/", json=data)
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test Company"


def test_get_company():
    # 首先创建一个公司
    create_data = {
        "name": "Test Company",
        "ticker": "TEST",
        "main_business": "Test Business",
        "employee_count": 100
    }
    create_response = requests.post(f"{BASE_URL}/companies/", json=create_data)
    assert create_response.status_code == 200
    company_id = create_response.json()["data"]["id"]

    # 然后获取该公司
    response = requests.get(f"{BASE_URL}/companies/{company_id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Test Company"


def test_list_companies():
    response = requests.get(f"{BASE_URL}/companies/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)


def test_update_company():
    # 首先创建一个公司
    create_data = {
        "name": "Test Company",
        "ticker": "TEST",
        "main_business": "Test Business",
        "employee_count": 100
    }
    create_response = requests.post(f"{BASE_URL}/companies/", json=create_data)
    assert create_response.status_code == 200
    company_id = create_response.json()["data"]["id"]

    # 然后更新该公司
    update_data = {
        "name": "Updated Company",
        "employee_count": 200
    }
    response = requests.put(f"{BASE_URL}/companies/{company_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated Company"
    assert response.json()["data"]["employee_count"] == 200


def test_delete_company():
    # 首先创建一个公司
    create_data = {
        "name": "Test Company",
        "ticker": "TEST",
        "main_business": "Test Business",
        "employee_count": 100
    }
    create_response = requests.post(f"{BASE_URL}/companies/", json=create_data)
    assert create_response.status_code == 200
    company_id = create_response.json()["data"]["id"]

    # 然后删除该公司
    response = requests.delete(f"{BASE_URL}/companies/{company_id}")
    assert response.status_code == 200

    # 验证是否已删除
    get_response = requests.get(f"{BASE_URL}/companies/{company_id}")
    assert get_response.status_code == 404
