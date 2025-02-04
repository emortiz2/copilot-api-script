import json
import csv

infile = '/Users/emortiz2/copilot-api-script/data/1-31.json'
daily_usage_metrics = '/Users/emortiz2/copilot-api-script/data/copilot_daily_metrics.csv'
ide_chat_metrics = '/Users/emortiz2/copilot-api-script/data/copilot_ide_chat_metrics.csv'
ide_code_completion_engagement = '/Users/emortiz2/copilot-api-script/data/copilot_ide_code_completion_engagement.csv'
ide_code_completion_metrics = '/Users/emortiz2/copilot-api-script/data/copilot_ide_code_completion_metrics.csv'

with open(infile, 'r') as f:
    data = json.load(f)

    daily_data = []
    ide_chat_data = []
    code_engagement_data = []
    code_metric_data = []
    for date_metrics in data:
        date = date_metrics['date']
        daily_data.append({
            'metric_date': date,
            'total_active_users': date_metrics['total_active_users'],
            'total_engaged_users': date_metrics['total_engaged_users']
        })

        for editor in date_metrics['copilot_ide_chat']['editors']:
            for model in editor['models']:
                ide_chat_data.append({
                    'metric_date': date,
                    'editor_name': editor['name'],
                    'model_name': model['name'],
                    'total_chats': model['total_chats'],
                    'is_custom_model': model['is_custom_model'],
                    'total_engaged_users': model['total_engaged_users'],
                    'total_chat_copy_events': model['total_chat_copy_events'],
                    'total_chat_insertion_events': model['total_chat_insertion_events']
                })

        for editor in date_metrics['copilot_ide_code_completions']['editors']:
            code_engagement_data.append({
                'metric_date': date,
                'editor_name': editor['name'],
                'total_engaged_users': editor['total_engaged_users']
            })

        for editor in date_metrics['copilot_ide_code_completions']['editors']:
            for model in editor['models']:
                for language in model['languages']:
                    code_metric_data.append({
                        'metric_date': date,
                        'editor_name': editor['name'],
                        'model_name': model['name'],
                        'is_custom_model': model['is_custom_model'],
                        'language_name': language['name'],
                        'total_engaged_users': language['total_engaged_users'],
                        'total_code_acceptances': language['total_code_acceptances'],
                        'total_code_suggestions': language['total_code_suggestions'],
                        'total_code_lines_accepted': language['total_code_lines_accepted'],
                        'total_code_lines_suggested': language['total_code_lines_suggested']
                    })

    with open(daily_usage_metrics, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['metric_date', 'total_active_users', 'total_engaged_users'])
        writer.writeheader()
        writer.writerows(daily_data)

    with open(ide_chat_metrics, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['metric_date', 'editor_name', 'model_name', 'total_chats', 'is_custom_model', 'total_engaged_users', 'total_chat_copy_events', 'total_chat_insertion_events'])
        writer.writeheader()
        writer.writerows(ide_chat_data)

    with open(ide_code_completion_engagement, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['metric_date', 'editor_name', 'total_engaged_users'])
        writer.writeheader()
        writer.writerows(code_engagement_data)

    with open(ide_code_completion_metrics, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['metric_date', 'editor_name', 'model_name', 'is_custom_model', 'language_name', 'total_engaged_users', 'total_code_acceptances', 'total_code_suggestions', 'total_code_lines_accepted', 'total_code_lines_suggested'])
        writer.writeheader()
        writer.writerows(code_metric_data)
    
