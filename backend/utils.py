import os
import shutil
import datetime

def row_to_json(row, columns, column_decoder=None):
    item = {}
    for column in columns:
        item[str(column)] = row[str(column)] if column_decoder is None \
                       else column_decoder(str(column), row[str(column)])

        if isinstance(item[str(column)], datetime.date):
            item[str(column)] = item[str(column)].isoformat()

        if isinstance(item[str(column)], set):
            item[str(column)] = list(item[str(column)])

    return item

def table_to_json(table, columns, column_decoder=None):
    data = []
    for row in table:
        data.append(row_to_json(row, columns, column_decoder=column_decoder))

    return data

def tree_to_ui(table):
    def parse_nodes(parents, table):
        new_parents = []
        for row in table:
            for parent in parents:
                if row['parent_id'] == parent['id']:
                    if 'children' not in parent.keys():
                        parent['children'] = []
                    parent['children'].append(row)
                    new_parents.append(row)

        if len(new_parents) != 0:
            parse_nodes(new_parents, table)

    data = [row for row in table if row['parent_id'] is None]
    parse_nodes(data, table)

    return data


class Email:
    delivery_intervals = [
        'с 12:00 до 15:00',
        'с 15:00 до 18:00',
        'с 18:00 до 21:00',
    ]

    payment_types = [
        'Наличными',
        'Переводом на Сбербанк курьеру',
    ]

    market_name = "Veggies"

    template = '''
<!DOCTYPE HTML PUBLIC «-//W3C//DTD HTML 4.0 Transitional//EN»>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta
                http-equiv="Content-Type"
                content="text/html; charset=UTF-8"
                />
        <title>{title}</title>
        <meta
                name="viewport"
                content="width=device-width,initial-scale=1.0"
                />
        <body>
        <table
                align="center"
                border="0"
                cellpadding="0"
                cellspacing="0"
                width="600"
                >
            <tr
                    align="center"
                    style="color: black; font-family: Arial, sans-serif;
                    font-size: 24px;"
                    >
                <td bgcolor="#e2ffbc" style="padding-top: 24px;
                        padding-bottom: 24px"
                        >
                    {toolbar}
                </td>
            </tr>
            <tr>
                <td bgcolor="#fffff5"
                        style="font-family: Arial, sans-serif;
                               vertical-align: top;
                               padding-top: 28px;
                               padding-right: 28px;
                               padding-bottom: 28px;
                               padding-left: 28px;"
                               height="500"
                        >
                    <span style="font-size: 18px">{header}</span>
                    {content}
                </td>
            </tr>
            <tr>
                <td
                        align="right"
                        bgcolor="#ffffff"
                        style="
                            color:#9e9e9e;
                            font-family:Arial,sans-serif;
                            font-size:14px;
                            padding-top:12px;
                            padding-bottom:12px;
                            padding-right:12px"
                        >
                    © Veggies
                </td>
            </tr>
    </head>
    '''

    delivery_info_template = '''
        <table style="font-size: 14px">
            <tr>
                <td style="padding-top: 12px;
                           padding-left: 12px;"
                        >
                    Доставим {delivery_date}
                    {delivery_interval}
                </td>
            </tr>
            <tr>
                    <td style="padding-left: 82px;">
                        {person_address}
                    </td>
            </tr>
            <tr>
                <td style="padding-bottom: 12px;
                           padding-left: 12px;"
                        >
                    Оплата {payment_type}{change_from}
                </td>
            </tr>
        </table>
    '''

    delivery_items_template = '''
        <table bgcolor="#ffffe0"
                style="border: 1px solid #f2f0b3;
                       border-radius: 2px;"
                >
            <tr>
                <td>
                    <table style="font-size: 16px" width="544">
                        {cart_items}
                    </table>
                </td>
            </tr>
            <tr style="border-top: 1px solid #efe823;">
                <td>
                    <table style="font-size: 18px;
                                  border-top: 1px solid #efe823;"
                            width="544"
                            >
                        <tr>
                            <td>
                                <span>{items_count},</span>
                                <span
                                        style="font-size: 12px;
                                               color: #9e9e9e;"
                                        >
                                    ≈{total_weight} кг
                                </span>
                            </td>
                            <td>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                К оплате
                            </td>
                            <td align="right">
                                {total_price}₽
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    '''

    @staticmethod
    def generate_items(cart, summary):
        items_templates = []
        template = '''
            <tr>
                <td style="color: #a09c08;">
                    {count} {name}
                </td>
                <td align="right">
                    {price}₽
                </td>
            </tr>
        '''
        for item in cart["items"]:
            items_templates.append(template.format(
                    count=item["count"],
                    name=Email.declension_text(
                        item["offerModel"]["entity"]["declensions"],
                        item["count"],
                        ),
                    price=item["offerModel"]["offer"]["price"] \
                            * item["count"],
                    ))

        items_templates.append('''
                <tr>
                    <td>
                        Выбор
                    </td>
                    <td align="right">
                        %s₽
                    </td>
                </tr>
                '''%summary['choice'])

        items_templates.append('''
                <tr>
                    <td>
                        Доставка
                    </td>
                    <td align="right">
                        %s₽
                    </td>
                </tr>
                '''%summary['delivery_price'])

        return '\n'.join(items_templates)

    @staticmethod
    def declension_text(declensions, count):
        if str(count)[-1] == '0' \
                or str(count)[-1] == '5' \
                or str(count)[-1] == '6' \
                or str(count)[-1] == '7' \
                or str(count)[-1] == '8' \
                or str(count)[-1] == '9' \
                or (len(str(count)) > 1 \
                    and str(count)[len(str(count))-2] == '1'):
            return declensions[2]
        elif str(count)[-1] == '1':
            return declensions[0]
        elif str(count)[-1] == '2' \
                or str(count)[-1] == '3' \
                or str(count)[-1] == '4':
            return declensions[1]

    @staticmethod
    def positions_text(items_count):
        return Email.declension_text([
            '%s позиция'%str(items_count),
            '%s позиции'%str(items_count),
            '%s позиций'%str(items_count),
            ], items_count)

    @staticmethod
    def order(cart, summary, order_id):
        delivery_info = Email.delivery_info_template.format(
                delivery_date='.'.join([
                        cart['deliveryDate'].split('-')[2],
                        cart['deliveryDate'].split('-')[1],
                        cart['deliveryDate'].split('-')[0],
                        ]),
                delivery_interval=cart['deliveryInterval'],
                person_address=cart['personAddress'],
                payment_type=cart['paymentType'].lower(),
                change_from='' if cart['paymentType'] == Email.payment_types[0] \
                               or 'changeFrom' not in cart.keys() \
                               or cart['changeFrom'] is None \
                               or cart['changeFrom'] == '' \
                               else ', change from %s₽'%cart['changeFrom'],
                )

        delivery_items = Email.delivery_items_template.format(
                cart_items=Email.generate_items(cart, summary),
                items_count=Email.positions_text(summary['count']),
                total_weight=summary['weight'],
                total_price=summary['amount'],
                )

        return Email.template.format(
                title='Veggies',
                toolbar='Veggies',
                header='Заказ №%s'%order_id,
                content=delivery_info+delivery_items,
                )

    @staticmethod
    def order_cancelled(order):
        return Email.template.format(
                title='Veggies',
                toolbar='Veggies',
                header='',
                content='''
                <table style="font-size: 14px">
                    <tr>
                        <td style="padding-top: 12px;
                                   padding-left: 12px;"
                                >
                            Заказ №%s отменён
                        </td>
                    </tr>
                </table>
                '''%order["id"],
                )

    @staticmethod
    def delivery_summary(summary, orders, delivery_date):
        items_templates = []
        total_price = 0
        total_weight = 0 
        for offer in summary:
            items_templates.append('''
                <tr>
                    <td style="color: #bfb90c;">
                        {count} {name}
                    </td>
                    <td align="right">
                        {price}₽
                    </td>
                </tr>
                '''.format(
                    count=offer["count"],
                    name=Email.declension_text(
                        offer["entity"]["declensions"],
                        offer["count"],
                        ),
                    price=offer["price"],
                    ))

            total_price += offer["price"]
            total_weight += offer["weight"] or 1


        delivery_items = Email.delivery_items_template.format(
                cart_items='\n'.join(items_templates),
                items_count=Email.positions_text(len(summary)),
                total_weight=total_weight,
                total_price=total_price,
                )

        intervals = [[],[],[]]
        order_items = []
        for model in orders:
            intervals[model["order"]["delivery_interval"]].append(
                    model["order"]["id"])

            order_items.append('''
                <tr>
                    <td style="padding-top: 12px;
                               padding-left: 12px;"
                            >
                        {offers}
                    </td>
                    <td style="padding-top: 12px;
                               padding-left: 12px;"
                            >
                        Заказ №{order_id}<br />

                        Сумма: {price}<br />
                        Тип оплаты: {payment_type}<br />
                        Сдача с: {change_from}<br />

                        Имя: {person_name}<br />
                        Телефон: {person_phone}<br />
                        Адрес: {person_address}<br />

                        Комментарий: {special_instructions}
                    </td>
                </tr>
            '''.format(
                offers='\n'.join(['''
                    %s %s<br />
                    '''%(
                        offer["count"], 
                        Email.declension_text(
                            offer["entity"]["declensions"],
                            offer["count"],
                            ),
                        ) for offer in model["offers"]]),
                order_id=model["order"]["id"],
                price=model["order"]["amount"],
                payment_type=Email.payment_types[
                    model["order"]["payment_type"]],
                change_from=model["order"]["change_from"],
                person_name=model["order"]["person_name"],
                person_phone=model["order"]["person_phone"],
                person_address=model["order"]["person_address"],
                special_instructions=model["order"]["special_instructions"],
                ))

        interval_items = []
        for idx in range(0, len(intervals)):
            interval_items.append('''
            <tr>
                <td style="padding-top: 12px;
                           padding-left: 12px;"
                        >
                    %s    
                </td>
                <td style="padding-top: 12px;
                           padding-left: 12px;"
                        >
                    %s    
                </td>
            </tr>
            '''%(Email.delivery_intervals[idx], ', '.join([
                    str(v) for v in intervals[idx]])))


        orders_info = '''
            <span style="font-size: 18px">Интервалы доставки</span>
            <table style="font-size: 14px">
                %s
            </table>
        '''%'\n'.join(interval_items)


        orders = '''
            <span style="font-size: 18px">Заказы</span>
            <table style="font-size: 14px">
                %s
            </table>
        '''%'\n'.join(order_items)

        return Email.template.format(
                title='Veggies',
                toolbar='Veggies',
                header='Доставка на %s'%str(delivery_date),
                content=delivery_items+orders_info+orders,
                )
