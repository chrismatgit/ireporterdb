class Intervention(object):
    reports = []
    def __init__(self, intervention_id, createdon, createdby, inctype, location, status, image, video,comment):
        self.intervention_id = intervention_id
        self.createdon = createdon
        self.createdby = createdby
        self.inctype = inctype
        self.location = location
        self.status = status
        self.image = image
        self.video = video
        self.comment = comment