#!/usr/bin/env python
# -*- coding: utf-8 -*-


def query_tuple_to_list(query_tuple, column_name):
    simple_list = [row[column_name] for row in query_tuple]
    return simple_list


def intersect_list(list1, list2):
    return [x for x in list1 if x in list2]


def substract_list(list1, list2):
    return [x for x in list1 if x not in list2]


def org_regex(org_list):
    org_regex_list = "|".join(org_list)
    regex = "(course-v1:|^)({orgs})[+/]".format(orgs=org_regex_list)
    return regex
