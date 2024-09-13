# def test_get_event_by_type_service(
#     client: TestClient,
# ):
#     r = client.get(
#         f"{settings.API_V1_STR}/event/get_by_type/1",
#     )
#     assert r.status_code == 200
#     events = r.json()["data"]
#     assert events
