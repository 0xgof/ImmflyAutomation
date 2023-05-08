
import test.ui_interaction as ui_interaction
import test.test_utils as test_utils
import logging

def basic_sorter_by_name_test():

    browser_manager = ui_interaction.BrowserManager()
    browser_manager.initialize_ui()
    browser_manager.sort_products('name')
    
    first_product_name = (browser_manager.get_first_product_name())
    second_product_name = (browser_manager.get_second_product_name())

    try:
        assert (test_utils.compare_words(first_product_name, second_product_name) == "word1 comes before word2 alphabetically")
        logging.info('BASIC SORTER BY NAME TEST PASSED')
        print('BASIC SORTER BY NAME TEST PASSED')
    except AssertionError:
        logging.info('BASIC SORTER BY NAME TEST FAILED')
        print('BASIC SORTER BY NAME TEST FAILED')
        print(f'First product name: {first_product_name}')
        print(f'Second product name: {second_product_name}')


def basic_sorter_default_state_test():

    browser_manager = ui_interaction.BrowserManager()
    browser_manager.initialize_ui()
    
    try:
        assert (browser_manager.get_products_order_state() == 'asc')
        logging.info('BASIC SORTER DEFAULT STATE TEST PASSED')
        print('BASIC SORTER DEFAULT STATE TEST PASSED')

    except AssertionError:
        logging.info('BASIC SORTER DEFAULT STATE TEST FAILED')
        print('BASIC SORTER DEFAULT STATE TEST FAILED')

    
def main():
    print('Running first test')
    basic_sorter_by_name_test()
    print('Running second test')
    basic_sorter_default_state_test()

if __name__ == "__main__":
    main()

