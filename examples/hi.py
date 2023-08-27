import pyspl

play = pyspl.Play('Hi? Hi.')

hamlet = play.character('Hamlet', 'a male.')
juliet = play.character('Juliet', 'a female.')

class ActI(pyspl.Act):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_scene(self.sceneI, 'I', 'The Only Scene.')

    def sceneI(self):
        self.enter(hamlet, juliet)
        self.set(juliet, pyspl.sum(64, 8))
        self.print(juliet, str)
        self.set(hamlet, pyspl.sum(juliet, pyspl.sum(32, 1)))
        self.print(hamlet, str)
        self.exit()

play.add_act(ActI(play), 'I', 'The Only Act.')

play.save('./play.spl')
