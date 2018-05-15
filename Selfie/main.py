import sys
from Farmware import *


class SelfieMaker(Farmware):
    def __init__(self):
        Farmware.__init__(self,((__file__.split(os.sep))[len(__file__.split(os.sep)) - 3]).replace('-master', ''))

    # ------------------------------------------------------------------------------------------------------------------
    # loads config parameters
    def load_config(self):
        prefix = self.app_name.lower().replace('-', '_')
        self.args={}
        self.args['topright']       = os.environ.get(prefix + '_topright', '(0, 130)')
        self.args['bottomleft']     = os.environ.get(prefix + '_bottomleft', '(2650, 1050)')
        self.args['stepsize']       = os.environ.get(prefix + '_stepsize', '(150, 150)')
        self.args['default_z']      = int(os.environ.get(prefix + '_default_z', 0))
        self.args['action']         = os.environ.get(prefix + '_action', 'test')

        try:
            self.args['topright'] = ast.literal_eval(self.args['topright'])
            self.args['bottomleft'] = ast.literal_eval(self.args['bottomleft'])
            self.args['stepsize'] = ast.literal_eval(self.args['stepsize'])

            if not isinstance(self.args['topright'], tuple):  raise ValueError
            if not isinstance(self.args['bottomleft'], tuple):  raise ValueError
            if not isinstance(self.args['stepsize'], tuple):  raise ValueError

        except:
            raise ValueError("Invalid value {},{} or {}".format(self.args['topright'], self.args['bottomleft'],self.args['stepsize']))

        if self.args['action'] != "real":
            self.log("TEST MODE, NO sequences or movement will be run, meta information will NOT be updated",'warn')
            self.debug=True

        self.log(str(self.args))

# ------------------------------------------------------------------------------------------------------------------
    def run(self):

        tool=None
        try:
            watering_tool = next(x for x in self.tools() if 'water' in x['name'].lower())
            tool = next(x for x in self.points() if x['pointer_type'] == 'ToolSlot' and x['tool_id'] == watering_tool['id'])
            points=ast.literal_eval(tool['meta']['selfie_cache'])
            if not isinstance(points, dict): raise ValueError
        except Exception as e:
            points={}

        try: photo = next(x for x in self.sequences() if x['name'] == 'take a photo')
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
                tool['meta']['selfie_cache']=str(points)
                self.post('points/{}'.format(tool['id']), tool)
                x += delta[0]
            y += delta[1]

        if tool!=None:
            del tool['meta']['selfie_cache']
            self.post('points/{}'.format(tool['id']),tool)

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
