# generate the page at some point
import os
import errno
import shutil
from wybory import env, data

# Wyniki wyborów w całym kraju plus mapka z województwami, na których można klikać
# Wyniki wyborów w każdym z województw plus odnośniki do okręgów
# Wyniki wyborów w każdym okręgu plus odnośniki do gmin
# Wyniki wyborów w każdej gminie w podziale na obwody

def build_kraj():
    my_list = filter(lambda x: x.nr_okregu == 1, data.Obwod.objects)

    template = env.get_template('index.html')
    out = template.render(my_list=my_list, go='here')
    with open(os.path.join('build/kraj.html'), "w+") as f:
        f.write(out)
        f.close()


def build_wojewodztwo(wojewodztwo_id):
    my_list = filter(lambda x: x.wojewodztwo_criteria_id == wojewodztwo_id, data.Obwod.objects)

    template = env.get_template('wojewodztwo.html')
    out = template.render(my_list=my_list, go='here')
    with open(os.path.join("build/woj{0}.html".format(wojewodztwo_id)), "w+") as f:
        f.write(out)
        f.close()
    return


def build_okreg(nr_okregu):
    my_list = filter(lambda x: x.nr_okregu == nr_okregu, data.Obwod.objects)

    template = env.get_template('okreg.html')
    out = template.render(my_list=my_list, go='here')
    with open(os.path.join("build/okr{0}.html".format(nr_okregu)), "w+") as f:
        f.write(out)
        f.close()
    return


def build_gmina(kod_gminy):
    my_list = filter(lambda x: x.kod_gminy == kod_gminy, data.Obwod.objects)

    template = env.get_template('gmina.html')
    out = template.render(my_list=my_list, go='here')
    with open(os.path.join("build/gm{0}.html".format(kod_gminy)), "w+") as f:
        f.write(out)
        f.close()
    return


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
    shutil.rmtree("build/", ignore_errors=True)
    make_sure_path_exists("build/")
    build_kraj()
    build_gmina('040802')
    build_gmina('080102')
    build_okreg(1)
    build_wojewodztwo(20853)

