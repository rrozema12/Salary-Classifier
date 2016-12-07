import naive_bayes as bayes
import table_utils
import file_system
import homework_util as homework
import constants
import partition
import output_util as output
import classifier_util
import hw4_util
import knn
import util


def _printExamples(table):
    """ Prints 5 example instances """
    test, training = partition.cut(table, 5)
    for instance in test:
        output.printInstance(instance)  # Print original instance

        # Calculate the actual and bayes predicted
        actual = instance[constants.INDICES['salary']]

        # change the instance to the values we are testing from
        instance = homework.getNamedTuples(instance, ['degree', 'ethnicity', 'gender'])
        predicted, probability = bayes.predict_label(training, instance, constants.INDICES['salary'])

        output.printClassActual(actual, predicted)  # Print results


def _printConfusionMatrix(labels, name):
    """ Prints a confusion matrix for given labels """
    output.printHeader('Confusion Matrix')
    hw4_util.print_confusion_matrix(labels, name)


def step_three(table):
    """ Analyzes the table based on Knn and Naive Bayes

    :param table: the table of the titanic dataset
    :return: nothing
    """

    table = table_utils.mapCol(table, constants.INDICES['job-type'],
                               homework.get_job_type)
    table = table_utils.mapCol(table, constants.INDICES['degree'],
                               homework.get_degree)
    table = table_utils.mapCol(table, constants.INDICES['marital-status'],
                               homework.get_marital_status)
    table = table_utils.mapCol(table, constants.INDICES['ethnicity'],
                               homework.get_ethnicity)
    table = table_utils.mapCol(table, constants.INDICES['gender'],
                               homework.get_gender)
    table = table_utils.mapCol(table, constants.INDICES['country'],
                               homework.get_country)
    table = table_utils.mapCol(table, constants.INDICES['salary'],
                               homework.get_salary)

    table = knn.normalize_table(table, [5,7])

    # KNN
    print('K_NN')

    labels = hw4_util.random_subsample_knn(table, 5, 10, constants.INDICES['salary'])
    accuracy = classifier_util.accuracy(labels)
    print('\tRandom Subsample (5)')
    print('\t\tAccuracy = ' + str(accuracy) + ', error rate = ' + str(1 - accuracy))

    labels = hw4_util.stratified_cross_fold_knn(table, 5, 10, constants.INDICES['salary'])

    accuracy = classifier_util.accuracy(labels)
    print('\tStratified Cross Folds (5)')
    print('\t\tAccuracy = ' + str(accuracy) + ', error rate = ' + str(1 - accuracy))
    _printConfusionMatrix(labels, 'Salary')

    # Naive Bayes
    print('\nNaive Bayes')
    test_by_names = ['degree', 'ethnicity', 'gender']

    accuracy = classifier_util.accuracy(
        hw4_util.random_subsample_naive_bayes(table, 10, constants.INDICES['salary'],
                                              test_by_names))

    print('\tRandom Subsample')
    print('\t\tAccuracy = ' + str(accuracy) + ', error rate = ' + str(1 - accuracy))

    labels = hw4_util.stratified_cross_fold_naive_bayes(table, 10, constants.INDICES['salary'],
                                                        test_by_names)
    accuracy = classifier_util.accuracy(labels)

    print('\tStratified CrossFolding')
    print('\t\tAccuracy = ' + str(accuracy) + ', error rate = ' + str(1 - accuracy))
    _printConfusionMatrix(labels, 'Salary')

def main():
    table = file_system.loadTable('incomeDataNoNA.csv')
    step_three(table)


if __name__ == "__main__":
    main()