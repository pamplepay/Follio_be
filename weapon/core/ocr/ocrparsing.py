# from weapon.core.ocr.LIG.ligmain import LIG_company_parsing
# from weapon.core.ocr.SAMSUNG.samsungmain import SAMSUNG_company_parsing
import json
import os
from weapon.core.ocr.ocrdata import Ocr_Data, LossInsurance, LifeInsurance
import re
from datetime import datetime

# def ocr_parsing(extract_data_list):
#     lst_result = None
#     if any("LIG" in item for item in extract_data_list):
#         cls_ocr_data = LIG_company_parsing(extract_data_list)
#     elif any("삼성" in item for item in extract_data_list):
#         cls_ocr_data = SAMSUNG_company_parsing(extract_data_list)

#     return cls_ocr_data

def is_number(value):
    return isinstance(value, (int, float))

def find_string_by_number(data_list, keyword, position):
    for data in data_list:
        # 키워드 위치 찾기
        keyword_index = data.find(keyword)

        if keyword_index != -1:
            if position < 0:  # 키워드 앞의 문자열을 찾음
                if position == -1:
                    # 키워드와 붙어있는 문자열 추출 (앞쪽)
                    pre_search = data[:keyword_index].strip()

                    # 마지막 공백 이후의 문자열 추출
                    last_space_index = pre_search.rfind(' ')
                    result = pre_search[last_space_index + 1:] if last_space_index != -1 else pre_search
                    return result
                else:
                    lst_data = data.split()
                    indexes = [index for index, element in enumerate(lst_data) if keyword in element]
                    search_index = indexes[0] + position + 1
                    return lst_data[search_index]
            else:
                if position == 1:
                    post_search = data[keyword_index + len(keyword):].strip()

                    # 첫 번째 공백 전까지의 문자열 추출
                    first_space_index = post_search.find(' ')
                    result = post_search[:first_space_index] if first_space_index != -1 else post_search
                    return result
                
                else:
                    lst_data = data.split()
                    search_index = lst_data.index(keyword) + position - 1
                    return lst_data[search_index]
    return None

def find_string_by_string(extract_data_list, search_word, search_split):
    # if 'R(' in search_split:
    #     loc_info = search_split.split(':')
    #     remove_word = loc_info[0][2:-1]
    #     for i, data in enumerate(extract_data_list):
    #         if search_word in data:
    #             if remove_word in data:
    #                 return None
    #             lst_part_data = []
    #             lst_part_data_length = len(loc_info)
    #             part_index = 1
    #             while part_index < lst_part_data_length:
    #                 lst_part_data.append(loc_info[part_index])
    #                 part_index = part_index + 1
    #             part_search_split = ':'.join(lst_part_data)
    #             result = find_string_by_string([data], search_word, part_search_split)
    #             return result
    #     return None
    
    if 'S(' in search_split:
        loc_info = search_split.split(':')
        if len(loc_info) == 4:
            up_and_down_offset = int(loc_info[0])
            left_and_right_offset = int(loc_info[1])
            split_char = loc_info[2][2:-1]  # S() 안의 문자 추출
            target_index = int(loc_info[3])

            for i, data in enumerate(extract_data_list):
                if search_word in data:
                    if up_and_down_offset != 0:
                        data = extract_data_list[i+up_and_down_offset]
                        lst_data = data.split()
                        find_data = lst_data[left_and_right_offset]
                        target_data = find_data.split(split_char)
                    else:
                        #lst_data = data.split(search_word)
                        search_word_index = data.index(search_word) + len(search_word)
                        if search_word_index < len(data):
                            lst_space_data = data.split(search_word)
                            lst_indexes = [index for index, item in enumerate(lst_space_data) if search_word in item]
                            if left_and_right_offset > 0:
                                result = find_string_by_number([lst_space_data[1]], split_char, target_index)
                            elif left_and_right_offset < 0:
                                result = find_string_by_number([lst_space_data[0]], split_char, target_index)
                        else:
                            # search_word_index = data.index(search_word)
                            # lst_data = data[:search_word_index].split()
                            search_word_index = data.index(search_word) + len(search_word)
                            if search_word_index < len(data):
                                lst_space_data = data.split(search_word)
                                lst_indexes = [index for index, item in enumerate(lst_space_data) if search_word in item]
                                if left_and_right_offset > 0:
                                    pass
                                elif left_and_right_offset < 0:
                                    result = find_string_by_number(lst_space_data, split_char, left_and_right_offset)
                    return result.strip()

        return None
                    
    elif '년 월 일' in search_split:
        loc_info = search_split.split(':')
        index_offset = int(loc_info[0])
        date_format = loc_info[1].split()
        target_index = int(loc_info[2])

        for i, data in enumerate(extract_data_list):
            if search_word in data:
                target_i = i + index_offset
                if 0 <= target_i < len(extract_data_list):
                    target_data = extract_data_list[target_i].split()
                    date_indices = [idx for idx, part in enumerate(target_data) if any(df in part for df in date_format)]
                    start_idx = date_indices[target_index*3]
                    result = ' '.join(target_data[start_idx:start_idx + len(date_format)])
                    # '년', '월'을 '.'로 대체하고, '일'을 제거
                    formatted_result = result.replace('년 ', '.').replace('월 ', '.').replace('일', '')
                    return formatted_result
    elif search_split.find(':') == 0:
        position = int(search_split[1:])
        for i, data in enumerate(extract_data_list):
            if search_word in data:
                keyword_index = data.find(search_word)
                if position == -1:
                    # 키워드와 붙어있는 문자열 추출 (앞쪽)
                    result = data[:keyword_index]
                    return result
                else:
                    result = data[:keyword_index+position+1]
                    return result
    elif search_split.find(':') > 0 and search_split.find('SPACE') > 0:
        lst_search_split = search_split.split(':')
        for data in extract_data_list:
            if search_word in data:
                start_index = data.find(search_word) + len(search_word) + int(lst_search_split[0])-1
                space_count = 0
                end_index = start_index

                # 다음 공백까지의 문자열 추출
                while space_count <= int(lst_search_split[2]) and end_index < len(data):
                    if data[end_index] == ' ':
                        space_count += 1
                    end_index += 1

                result = data[start_index:end_index].strip()
                return result
    elif search_split.find(':') > 0:
        lst_search_split = search_split.split(':')
        up_and_down_offset = int(lst_search_split[0])
        left_and_right_offset = int(lst_search_split[1])
        for i, data in enumerate(extract_data_list):
                if search_word in data:
                    if up_and_down_offset != 0:
                        data = extract_data_list[i+up_and_down_offset]
                        lst_data = data.split()
                        result = lst_data[left_and_right_offset]
                        return result


# extract_data_list : ocr에서 읽은 전체 데이터
# dict_detail_data : 화면에 보여주기 위해 저장할 카테고리
# arr_detail_data : json을 중심으로 파싱하기 위한 규격 및 정의
def find_detail_data(extract_data_list, lst_check_use_data, dict_detail_data, arr_detail_data):
    #try:
        for i, data in enumerate(extract_data_list):
            # lst_detail_data의 모든 원소가 data 문자열 안에 있는지 확인
            if lst_check_use_data[i] == 1:
                continue
            lst_detail_data_species = arr_detail_data['분류'].split()
            all_exist = all(element in data for element in lst_detail_data_species)
            if all_exist == True:
                lst_class_value = arr_detail_data['위치'].split('->')
                str_first_value = lst_class_value[0].replace(' ', '')
                if str_first_value in dict_detail_data:
                    str_sub_value = lst_class_value[1]
                    if str_sub_value in dict_detail_data[str_first_value]:
                        str_total_value = lst_class_value[2]
                        str_value = ''
                        key_exists = any("납입기간" in item for item in arr_detail_data.keys())
                        if key_exists == True:
                            try:
                                search_word = arr_detail_data['납입기간']
                                if is_number(arr_detail_data['납입기간_LOC']):
                                    data_pos = arr_detail_data['납입기간_LOC']
                                    payment_period_data = int(find_string_by_number([data], search_word, data_pos))
                                    payment_period_unit = arr_detail_data['납입기간단위']
                                    str_value = f'{payment_period_data}:{payment_period_unit}'
                            except:
                                break 

                        key_exists = any("보장기간" in item for item in arr_detail_data.keys())
                        if key_exists == True:
                            try:
                                search_word = arr_detail_data['보장기간']
                                if is_number(arr_detail_data['보장기간_LOC']):
                                    data_pos = arr_detail_data['보장기간_LOC']
                                    coverage_period_data = int(find_string_by_number([data], search_word, data_pos))
                                else:
                                    search_split = arr_detail_data['보장기간_LOC']
                                    coverage_period_data = int(find_string_by_string([data], search_word, search_split))
                                coverage_period_unit = arr_detail_data['보장기간단위']
                                str_value = f'{str_value}:{coverage_period_data}:{coverage_period_unit}'
                            except:
                                break 
                        key_exists = any("보장금액" in item for item in arr_detail_data.keys())
                        if key_exists == True:
                            try:
                                if arr_detail_data['보장금액'] == 'last':
                                    lst_data = data.split()
                                    str_coverage_amount = lst_data[-1].replace(',', '').replace('원', '').replace('(', '').replace(')', '')
                                    coverage_amount = int(str_coverage_amount)
                                else:
                                    search_word = arr_detail_data['보장금액']
                                    if is_number(arr_detail_data['보장금액_LOC']):
                                        data_pos = arr_detail_data['보장금액_LOC']
                                        coverage_period_data = find_string_by_number([data], search_word, data_pos)
                                        str_coverage_amount = coverage_period_data.replace(',', '').replace('원', '').replace('(', '').replace(')', '')
                                        coverage_amount = int(str_coverage_amount)
                            except:
                                break 
                        
                        str_value = f'{str_value}:{coverage_amount}'
                        dict_detail_data[str_first_value][str_sub_value][str_total_value].append(str_value)
                        lst_check_use_data[i] = 1
        return
    # except:
    #     print("ERROR!!!!!!!!!!!!!!!")
    #     return


def add_asterisks(search_data):
    # '-1' 또는 '-2' 뒤의 위치 찾기
    index_1 = search_data.find('-1')
    index_2 = search_data.find('-2')

    # 가장 마지막 위치 결정 (둘 중 하나는 -1이 될 수 있음)
    index = max(index_1, index_2)

    # ')' 바로 앞의 공백 제거
    search_data = search_data.replace(' )', ')')

    if index != -1:
        # '-1' 또는 '-2' 다음의 부분을 추출
        part_after = search_data[index + 2:]

        # '*'의 개수 세기
        asterisk_count = part_after.count('*')

        # '*'가 6개 미만이면 필요한 만큼 추가
        if asterisk_count < 6:
            additional_asterisks = '*' * (6 - asterisk_count)
            search_data = search_data[:index + 2] + additional_asterisks + part_after.lstrip('*')

    return search_data

def get_ocr_data(extract_data_list, ocr_data):
    ocrdata = Ocr_Data()
    if ocr_data['보험종류'] == 0:
        life_company = ocr_data['생명보험']
        ocrdata.dict_life_head_data['생명보험'] = LifeInsurance.company.index(life_company)
        ocrdata.dict_life_head_data['상품명'] = ocr_data['상품명']
        search_word = ocr_data['계약자']
        if is_number(ocr_data['계약자_LOC']):
            pass
        else:      
            # search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            # modified_data = add_asterisks(search_data)
            data_pos = ocr_data['계약자_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            ocrdata.dict_life_head_data['계약자'] = search_data
        search_word = ocr_data['납입기간']
        if is_number(ocr_data['납입기간_LOC']):
            pass
        else:
            data_pos = ocr_data['납입기간_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            search_data = search_data.replace(' ', '')
            # '~' 또는 '-'를 기준으로 날짜 분리
            dates = re.split('~|-', search_data)

            # 정규 표현식을 사용하여 날짜 형식 확인 및 변경
            for i in range(len(dates)):
                if not re.match(r'\d{4}\.\d{2}\.\d{2}', dates[i]):
                    dates[i] = "0000.00.00"

            # 날짜 포맷 변경
            date_format = "%Y.%m.%d"
            date1 = datetime.strptime(dates[0], date_format)
            date2 = datetime.strptime(dates[1], date_format)

            # 년수 차이 계산
            year_difference = abs(date2.year - date1.year)
            ocrdata.dict_life_head_data['납입기간'] = year_difference
            ocrdata.dict_life_head_data['계약일'] = dates[0]
            ocrdata.dict_life_head_data['만기일'] = dates[1]
            

        search_word = ocr_data['피보험자']
        if is_number(ocr_data['피보험자_LOC']):
            data_pos = ocr_data['피보험자_LOC']
            search_data = find_string_by_number(extract_data_list, search_word, data_pos)
            ocrdata.dict_life_head_data['피보험자'] = search_data

        search_word = ocr_data['보장기간']
        try:
            if is_number(ocr_data['보장기간_LOC']):
                pass
            else:
                pass
        except KeyError as e:
            ocrdata.dict_life_head_data['보장기간'] = search_word
            
        search_word = ocr_data['월납입보험료']
        if is_number(ocr_data['월납입보험료_LOC']):
            pass
        else:
            data_pos = ocr_data['월납입보험료_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            ocrdata.dict_loss_head_data['피보험자'] = search_data

    else:
        loss_company = ocr_data['손해보험']
        ocrdata.dict_loss_head_data['손해보험'] = LossInsurance.company.index(loss_company)
        ocrdata.dict_loss_head_data['상품명'] = ocr_data['상품명']
        search_word = ocr_data['계약자']
        if is_number(ocr_data['계약자_LOC']):
            data_pos = ocr_data['계약자_LOC']
            search_data = find_string_by_number(extract_data_list, search_word, data_pos)
            ocrdata.dict_loss_head_data['계약자'] = search_data
        else:
            # search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            # modified_data = add_asterisks(search_data)
            data_pos = ocr_data['계약자_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            ocrdata.dict_loss_head_data['계약자'] = search_data

        search_word = ocr_data['납입기간']
        if is_number(ocr_data['납입기간_LOC']):
            data_pos = ocr_data['납입기간_LOC']
            search_data = find_string_by_number(extract_data_list, search_word, data_pos)
            ocrdata.dict_loss_head_data['납입기간'] = int(search_data)
        else:
            data_pos = ocr_data['납입기간_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            search_data = search_data.replace(' ', '')
            # '~' 또는 '-'를 기준으로 날짜 분리
            dates = re.split('~|-', search_data)

            # 정규 표현식을 사용하여 날짜 형식 확인 및 변경
            for i in range(len(dates)):
                if not re.match(r'\d{4}\.\d{2}\.\d{2}', dates[i]):
                    dates[i] = "0000.00.00"

            # 날짜 포맷 변경
            date_format = "%Y.%m.%d"
            date1 = datetime.strptime(dates[0], date_format)
            date2 = datetime.strptime(dates[1], date_format)

            # 년수 차이 계산
            year_difference = abs(date2.year - date1.year)
            ocrdata.dict_loss_head_data['납입기간'] = year_difference
            ocrdata.dict_loss_head_data['계약일'] = dates[0]
            ocrdata.dict_loss_head_data['만기일'] = dates[1]

        search_word = ocr_data['피보험자']
        if is_number(ocr_data['피보험자_LOC']):
            data_pos = ocr_data['피보험자_LOC']
            search_data = find_string_by_number(extract_data_list, search_word, data_pos)
            ocrdata.dict_loss_head_data['피보험자'] = search_data
        else:
            search_split = ocr_data['피보험자_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, search_split)
            ocrdata.dict_loss_head_data['피보험자'] = search_data

        search_word = ocr_data['보장기간']
        try:
            if is_number(ocr_data['보장기간_LOC']):
                data_pos = ocr_data['보장기간_LOC']
                search_data = find_string_by_number(extract_data_list, search_word, data_pos)
                ocrdata.dict_loss_head_data['보장기간'] = int(search_data)
        except KeyError as e:
            ocrdata.dict_loss_head_data['보장기간'] = search_word

        search_word = ocr_data['월보장보험료']
        if is_number(ocr_data['월보장보험료_LOC']):
            data_pos = ocr_data['월보장보험료_LOC']
            search_data = find_string_by_number(extract_data_list, search_word, data_pos)
            # ','와 '원' 문자 제거
            search_data = search_data.replace(',', '').replace('원', '').replace('(', '').replace(')', '')
            ocrdata.dict_loss_head_data['월보장보험료'] = int(search_data)
        else:
            data_pos = ocr_data['월보장보험료_LOC']
            search_data = find_string_by_string(extract_data_list, search_word, data_pos)
            search_data = search_data.replace(',', '').replace('원', '').replace('(', '').replace(')', '')
            ocrdata.dict_loss_head_data['월보장보험료'] = int(search_data)

        try:
            search_word = ocr_data['계약일']
            if is_number(ocr_data['계약일_LOC']):
                pass
            else:
                search_split = ocr_data['계약일_LOC']
                search_data = find_string_by_string(extract_data_list, search_word, search_split)
                ocrdata.dict_loss_head_data['계약일'] = search_data
        except KeyError as e:
            pass

        try:
            search_word = ocr_data['만기일']
            if is_number(ocr_data['만기일_LOC']):
                pass
            else:
                search_split = ocr_data['만기일_LOC']
                search_data = find_string_by_string(extract_data_list, search_word, search_split)
                ocrdata.dict_loss_head_data['만기일'] = search_data
        except KeyError as e:
            pass
        
        try:
            search_word = ocr_data['월적립보험료']
            if is_number(ocr_data['월적립보험료_LOC']):
                data_pos = ocr_data['월적립보험료_LOC']
                search_data = find_string_by_number(extract_data_list, search_word, data_pos)
                # ','와 '원' 문자 제거
                search_data = search_data.replace(',', '').replace('원', '').replace('(', '').replace(')', '')
                ocrdata.dict_loss_head_data['월적립보험료'] = int(search_data)
            else:
                data_pos = ocr_data['월적립보험료_LOC']
                search_data = find_string_by_string(extract_data_list, search_word, data_pos)
                search_data = search_data.replace(',', '').replace('원', '').replace('(', '').replace(')', '')
                ocrdata.dict_loss_head_data['월적립보험료'] = int(search_data)
        except KeyError as e:
            pass

        # 담보별 세부사항
        try:
            arr_detail_data = ocr_data['세부사항']
            # 분류가 긴 순서대로 정렬
            sorted_arr_detail_data = sorted(arr_detail_data, key=lambda d: -len(d['분류']))
            # extract_data_list의 길이만큼 0으로 채워진 새로운 리스트 생성
            lst_check_use_data = [0 for _ in extract_data_list]
            for detail_data in sorted_arr_detail_data:
                find_detail_data(extract_data_list, lst_check_use_data, ocrdata.dict_detail_data, detail_data)
        except KeyError as e:
            pass

    return ocrdata




def ocr_parsing(extract_data_list):
    current_path = os.getcwd()
    jsonpath = os.path.join(current_path, 'ocrdata/insurancelist/list.json')
    
    with open(jsonpath, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # 상품명이 extract_data_list에 포함되어 있는 경우 해당 위치 반환
    str_location = ''
    for product in json_data["보험"]:
        product_name = product["상품명"]
        for extracted_text in extract_data_list:
            if product_name in extracted_text:
                str_location = product["위치"]

    insurance_json_path = os.path.join(current_path, str_location)
    with open(insurance_json_path, 'r', encoding='utf-8') as file:
        ocr_data = json.load(file)

    cls_ocr_data = get_ocr_data(extract_data_list, ocr_data)
    return cls_ocr_data


    