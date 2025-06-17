import time


def get_date_time(date, mode=1):
    # if mode<>1: strftime '11.04.24.01.24' as '11 апреля 2024г. 01:24'
    # if mode=1: strftime '11.04.24.01.24' as
    #    '11 апреля 2024г.
    #         01:24'

    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    date_list = date.split('.')
    if mode == 1:
        chr_ = chr(10)
    else:
        chr_ = ''
    text_time = (
        date_list[0] + ' ' + month_list[int(date_list[1]) - 1] +
        ' ' + date_list[2] + 'г. ' + chr_ + date_list[3] + ':' + date_list[4])
    return text_time


if __name__ == '__main__':
    newtime = time.strftime('%d.%m.%Y.%H.%M')
    print(get_date_time(newtime, 2))
