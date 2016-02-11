import scripts
import argparse

def test_seed_db(db_name):
    test_db = scripts.seed_db(db_name)

    # available options:
    #     attribute_definitions
    #     creation_date_time
    #     global_secondary_indexes
    #     item_count
    #     key_schema
    #     latest_stream_arn
    #     latest_stream_label
    #     local_secondary_indexes
    #     provisioned_throughput
    #     stream_specification
    #     table_arn
    #     table_name
    #     table_size_bytes
    #     table_status
    response = {'name': test_db.table_name, 'arn': test_db.table_arn}
    return response

def parse_args():
    
    return args

def main():
    # args = parse_args()
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", nargs='?', default="run_all")
    parser.add_argument("-n", "--name", nargs='?', default="test_hackpsu_table")
    args = vars(parser.parse_args())

    test_results = {}
    if args['test'] == 'run_all':
        value = test_seed_db(db_name=args['name'])
        test_results.update({'seed_db': value})
    elif args['test'] == 'seed_db':
        value = test_seed_db(db_name=args['name'])
        test_results.update({'seed_db': value})
    else:
        print(args)

    print(test_results)


if __name__ == '__main__':
    main()
