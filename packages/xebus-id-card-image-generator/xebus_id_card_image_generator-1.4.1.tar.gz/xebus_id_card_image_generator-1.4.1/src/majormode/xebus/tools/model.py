# Copyright (C) 2020 Majormode.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Majormode | one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement | other applicable agreement you
# entered into with Majormode.
#
# MAJORMODE MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY
# OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE, OR NON-INFRINGEMENT.  MAJORMODE SHALL NOT BE LIABLE FOR ANY
# LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING
# OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations


class IdCardInfo:
    def __init__(
            self,
            account_sis_id: str,
            full_name: str,
            class_name: str | None = None,
            first_name: str | None = None,
            grade_level: int | None = None,
            grade_name: str | None = None,
            last_name: str | None = None
    ):
        """
        Build the ID card of a person.


        :param account_sis_id: The child's identifier as recorded in the
            School Information System (SIS) of the organization managing this
            child.

        :param full_name: The complete personal name by which the card owner
            is known, including their surname, forename and middle name(s), in
            the correct lexical name order depending on the culture of this
            person.

        :param class_name: The name of the child's class.

        :param first_name: The forename of the child.

        :param grade_level: The education grade level that the child has
            reached for the current or the coming school year.  It generally
            corresponds to the number of the year a pupil has reached in this
            given educational stage for this grade.

        :param grade_name: The name of the educational grade that the child
            has reached for the current or the coming school year.

        :param last_name: The surname of the child.
        """
        self.__account_sis_id = account_sis_id

        self.__first_name = first_name
        self.__last_name = last_name
        self.__full_name = full_name

        self.__grade_level = grade_level
        self.__grade_name = grade_name

        self.__class_name = class_name

    @property
    def account_sis_id(self) -> str:
        return self.__account_sis_id

    @property
    def class_name(self) -> str | None:
        return self.__class_name

    @property
    def first_name(self) -> str | None:
        return self.__first_name

    @property
    def full_name(self) -> str | None:
        return self.__full_name

    @property
    def grade_level(self) -> int | None:
        return self.__grade_level

    @property
    def grade_name(self) -> str | None:
        return self.__grade_name

    @property
    def last_name(self) -> str | None:
        return self.__last_name
