import sys
from Farmware import *


class SelfieMaker(Farmware):
    def __init__(self):
        Farmware.__init__(self,((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', ''))

    # ------------------------------------------------------------------------------------------------------------------
    # loads config parameters
    def load_config(self):

        super(SelfieMaker,self).load_config()

        self.get_arg('topright', (0, 130))
        self.get_arg('bottomleft', (2650, 1050))
        self.get_arg('stepsize', (150, 150))
        self.get_arg('default_z', 0)
        self.get_arg('action', 'local')

        self.log(str(self.args))

# ------------------------------------------------------------------------------------------------------------------
    def run(self):

        try:
            watering_tool = next(x for x in self.tools() if 'water' in x['name'].lower())
            tool = next(x for x in self.points() if x['pointer_type'] == 'ToolSlot' and x['tool_id'] == watering_tool['id'])
            points=ast.literal_eval(tool['meta']['selfie_cache'])
            if not isinstance(points, dict): raise ValueError
            self.log("Selfie cache will be saved to tool id {}".format(tool['id']))
        except Exception as e:
            tool=None
            self.log('Watering tool is not found, selfie_cache will not be saved, if you restart the farmware - '
                     'it will start from the beginning','warn')
            points={}

        try: photo = next(x for x in self.sequences() if x['name'].lower() == 'take a photo')
        except: raise ValueError("Unable to find sequence TAKE A PHOTO, create one!")

        tr = self.args['topright']
        bl = self.args['bottomleft']
        max_d = self.args['stepsize']
        z = self.args['default_z']


        steps=[0,0]
        delta=[0,0]
        steps[0]=int((bl[0]-tr[0])/max_d[0])
        steps[1] = int((bl[1] - tr[1])/ max_d[1])
        delta[0] =int((bl[0]-tr[0])/steps[0])
        delta[1] = int((bl[1] - tr[1]) / steps[1])

        y = tr[1]
        for j in range(0,steps[1]+1):
            x = tr[0]
            for i in range (0,steps[0]+1):
                key="({},{})".format(x,y)
                if  key not in points or today_utc()-l2d(points[key])> datetime.timedelta(hours=1):
                    self.move_absolute({'x': x, 'y': y, 'z': z})
                    start=today_utc()
                    self.execute_sequence(photo)
                    duration=today_utc()-start
                    if duration>datetime.timedelta(seconds=20):
                        self.log('Camera produced black image, is not it?','error')
                        exit(1)
                else:
                    self.log('{} skipped as it was already taken less than 1h ago'.format(key))

                points["({},{})".format(x,y)]=d2l(today_utc())
                if tool != None:
                    tool['meta']['selfie_cache']=str(points)
                    self.put('points/{}'.format(tool['id']), tool)
                x += delta[0]
            y += delta[1]

        if tool!=None:
            if 'selfie_cache' in tool['meta']: del tool['meta']['selfie_cache']
            self.put('points/{}'.format(tool['id']),tool)

        self.move_absolute({'x': tr[0], 'y': tr[1], 'z': z})

# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    app = SelfieMaker()
    try:
        app.load_config()
        app.run()
        sys.exit(0)

    except NameError as error:
        app.log('SYNTAX!: {}'.format(str(error)), 'error')
        raise
    except requests.exceptions.HTTPError as error:
        app.log('HTTP error {} {} '.format(error.response.status_code,error.response.text[0:100]), 'error')
    except Exception as e:
        app.log('Something went wrong: {}'.format(str(e)), 'error')
    sys.exit(1)
