# generate the page at some point
import os
import errno
import shutil
from wybory import env, data
from  more_itertools import unique_everseen

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
    html_name = "woj{0}.html".format(wojewodztwo_id)
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    wojewodztwo_list = filter(lambda x: x.wojewodztwo_criteria_id == wojewodztwo_id, data.Obwod.objects)
    children = list(unique_everseen(wojewodztwo_list, lambda x: x.nr_okregu))
    children_links = dict(map(lambda x: ("Okreg {0}".format(int(x.nr_okregu)), build_okreg(x.nr_okregu)), children))

    template = env.get_template('wojewodztwo.html')
    out = template.render(my_dict=children_links, go='here')
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()

    return html_name


def build_okreg(nr_okregu):
    html_name = "okr{0}.html".format(int(nr_okregu))
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    okreg_list = filter(lambda x: x.nr_okregu == nr_okregu, data.Obwod.objects)
    children = list(unique_everseen(okreg_list, lambda x: x.kod_gminy))
    children_links = dict(map(lambda x: (x.gmina, build_gmina(x.kod_gminy)), children))

    template = env.get_template('okreg.html')
    out = template.render(my_dict=children_links)
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()

    return html_name


def build_gmina(kod_gminy):
    html_name = "gm{0}.html".format(kod_gminy)
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    gmina_list = filter(lambda x: x.kod_gminy == kod_gminy, data.Obwod.objects)
    obwod_list = list(unique_everseen(map(lambda x: x.nr_obwodu, gmina_list)))

    template = env.get_template('gmina.html')
    out = template.render(my_list=gmina_list, go='here')
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()

    return html_name


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


if __name__ == "__main__":
    shutil.rmtree("build/", ignore_errors=True)
    make_sure_path_exists("build/")
    build_wojewodztwo(20853)

