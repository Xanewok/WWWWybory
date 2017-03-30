# generate the page at some point
import os
import errno
import shutil
from collections import OrderedDict

from wybory import env, data
from  more_itertools import unique_everseen

# Wyniki wyborów w całym kraju plus mapka z województwami, na których można klikać
# Wyniki wyborów w każdym z województw plus odnośniki do okręgów
# Wyniki wyborów w każdym okręgu plus odnośniki do gmin
# Wyniki wyborów w każdej gminie w podziale na obwody

def build_kraj():
    html_name = "kraj.html"

    for woj_id in data.polish_province_ids():
        build_wojewodztwo(woj_id)

    result_set = data.calculate_result_set(data.Obwod.objects)

    template = env.get_template('kraj.html')
    out = template.render(result_set=result_set)
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()


def build_wojewodztwo(wojewodztwo_id):
    html_name = "woj{0}.html".format(wojewodztwo_id)
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    wojewodztwo_list = filter(lambda x: x.wojewodztwo_criteria_id == wojewodztwo_id, data.Obwod.objects)
    children = sorted(list(unique_everseen(wojewodztwo_list, lambda x: x.nr_okregu)), key=lambda x: x.nr_okregu)
    children_links = OrderedDict(map(lambda x: ("Okręg {0}".format(x.nr_okregu), build_okreg(x.nr_okregu)), children))

    wojewodztwo_list = filter(lambda x: x.wojewodztwo_criteria_id == wojewodztwo_id, data.Obwod.objects)
    result_set = data.calculate_result_set(wojewodztwo_list)

    template = env.get_template('wojewodztwo.html')
    out = template.render(my_dict=children_links, result_set=result_set)
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()

    return html_name


def build_okreg(nr_okregu):
    html_name = "okr{0}.html".format(nr_okregu)
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    okreg_list = filter(lambda x: x.nr_okregu == nr_okregu, data.Obwod.objects)
    children = sorted(list(unique_everseen(okreg_list, lambda x: x.kod_gminy)), key=lambda x: x.gmina)
    children_links = OrderedDict(map(lambda x: (x.gmina, build_gmina(x.kod_gminy)), children))

    okreg_list = filter(lambda x: x.nr_okregu == nr_okregu, data.Obwod.objects)
    result_set = data.calculate_result_set(okreg_list)

    template = env.get_template('okreg.html')
    out = template.render(my_dict=children_links, result_set=result_set)
    with open("build/" + html_name, "w+") as f:
        f.write(out)
        f.close()

    return html_name


def build_gmina(kod_gminy):
    html_name = "gm{0}.html".format(kod_gminy)
    if os.path.isfile("build/" + html_name): # Don't rerender if not needed
        return html_name

    gmina_list = filter(lambda x: x.kod_gminy == kod_gminy, data.Obwod.objects)
    results = OrderedDict(map(lambda x: (x, list(data.calculate_result_set([x]))), gmina_list))

    template = env.get_template('gmina.html')
    out = template.render(my_list=gmina_list, result_set=results)
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
    shutil.copyfile("resources/style.css", "build/style.css")
    build_kraj()

