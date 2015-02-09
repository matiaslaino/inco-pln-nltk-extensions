import pickle

__author__ = 'Matias'


class ConfigurationManager:
    settings_file_name = "settings.txt"

    @staticmethod
    def save(freeling_path, treetagger_path, maltparser_path, maltparser_model_path):
        settings_file = open(ConfigurationManager.settings_file_name, mode='wb')

        config = {'freeling_path': freeling_path, 'treetagger_path': treetagger_path,
                  'maltparser_path': maltparser_path, 'maltparser_model_path': maltparser_model_path}

        pickle.dump(config, settings_file)

    @staticmethod
    def load():
        try:
            settings_file = open(ConfigurationManager.settings_file_name, mode='r')

            config = pickle.load(settings_file)
        except:
            config = {'freeling_path': '', 'treetagger_path': '',
                      'maltparser_path': '', 'maltparser_model_path': ''}

        return config