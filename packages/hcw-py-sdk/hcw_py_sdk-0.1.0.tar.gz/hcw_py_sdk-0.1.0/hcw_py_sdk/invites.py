from .req import authRequests


class Invites:

    def __init__(self, req: authRequests):
        self.req = req
        self.url = f"{self.req.base_url}/invite"

    @property
    def list(self) -> list:

        return self.req.get(url=self.url)

    def create(self, **info):
        r = {
            "url": self.url,
            "json": {
                "emailAddress": info.get("emailAddress"),
                "doctorLanguage": info.get("doctorLanguage"),
                "firstName": info.get("firstName"),
                "lastName": info.get("lastName"),
                "gender": info.get("gender"),
                "patientTZ": info.get("patientTZ"),
                "sendInvite": info.get("sendInvite"),
                "isPatientInvite": info.get("isPatientInvite"),
            }
        }
        return self.req.post(**r)

    def delete(self, id):
        r = {
            "url": f"{self.url}/{id}",
        }
        return self.req.delete(**r)
