import subprocess
import csv
import os
import json


# take data_dir and output list of files inside of it 
# includes multiple variations, adapted for different
def get_image_files(data_dir):
    files = os.listdir(data_dir)
    files_shorter = []
    for i in range(0, len(files), 100):
        file_100 = files[i]
        files_shorter.append(file_100)
    cleaned_files = []
    for f in files:
        if f not in files_shorter:
            cleaned_files.append(f)

    files_shorter2 = []
    for i in range(1, len(cleaned_files), 40):
        file_40 = files[i]
        files_shorter2.append(file_40)
    return cleaned_files

# combine prediction files (outputted as a result of running on 2 devices)
def combine_prediction_files():
    file1 = './predictions_98_batches.csv'
    file2 = './predictionsND.csv'
    with open(file1,'r') as csvinput:
        with open(file2,'r') as csvinput2:
            with open("./predictions_all.csv", 'w') as csvoutput:
                writer = csv.writer(csvoutput)
                reader = csv.reader(csvinput)
                reader2 = csv.reader(csvinput2)

                all = []
                header = next(reader)
                header2 = next(reader2)
                all.append(header)

                for row in reader:
                    row2 = next(reader2)
                    filename1 = row[0]
                    filename2 = row2[0]
                    if row2[5] != '' and row[5] != '' and row[5] == row2[5]:
                        print(filename1)
                        all.append(row)
                    elif row2[5] != '':
                        all.append(row2)
                    elif row[5] != '':
                        all.append(row)
                writer.writerows(all)



# create an empty preidctions file with the proper headers 
# and empty strings in place of the predicted_label and predicted_prob
def create_empty_predictions_file(input_csv):
    with open(input_csv,'r') as csvinput:
        with open("./predictions_0_batches.csv", 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)
            

            all = []
            header = next(reader)
            
            all.append(header)

            for row in reader:
                filename = row[0]
                predicted_label = ""
                predicted_prob = ""
                row.append(predicted_label)
                row.append(predicted_prob)
                all.append(row)

            writer.writerows(all)

# take results of classifying 100 images (predictions_dict) and add to previous predicitons file
# write combined results to a new predictions file (labeled with the batch number)
def batch_write_to_csv(dict_predictions, previous_predictions_csv, num_batches):
    output_file = "./predictions_" + str(num_batches) + "_batches.csv"
    with open(previous_predictions_csv,'r') as csvinput:
        with open(output_file, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            header = next(reader)
            all.append(header)

            filenames = dict_predictions.keys()
            for row in reader:
                filename = row[0]
                if filename in filenames:
                    predicted_label = dict_predictions[filename][0]
                    predicted_prob = dict_predictions[filename][1]
                    row[4] = predicted_label
                    row[5] = float(predicted_prob.strip("\n"))
                all.append(row)

            writer.writerows(all)


# takes list of image names as input and 
# classifies each image, parses output
# every 100 images, writes to csv
# key = image name (train/ + image_name.jpg), value = [M or F, prob]
def classify_and_record(data_dir, image_filenames):
    files = image_filenames

    command = 'python guess.py --class_type gender --model_type pretrained_model --model_dir ./inception/21936/ --filename ' + './' + data_dir + '/'
    num_files = len(files)

    count_in_mem = 0
    dict_predictions = {}

    num_batches = 0
    
    for filename in files:
        new_command = command + filename
        result = subprocess.run(new_command.split(), stdout=subprocess.PIPE)
        
        output = result.stdout.decode('utf-8')
        
        dict_predictions[filename] = parse_classifier_output(output)
        count_in_mem += 1

        if count_in_mem >= 100:
            num_batches += 1
            previous_predictions_csv = "./predictions_" + str(num_batches-1) + "_batches.csv"

            batch_write_to_csv(dict_predictions, previous_predictions_csv, num_batches)
            # reset count and dictionary of predictions from this batchHi 
            count_in_mem = 0
            dict_predictions = {}
        
        print("Done with " + filename)
        index = files.index(filename)
        print("done with " + str(index+1) + " out of " + str(num_files))

    print ("FINISHED with this many files: ")
    print (len(dict_predictions.keys()))

# takes list of image names as input and 
# outputs dictionary with 
# key = image name (train/ + image_name.jpg), value = [M or F, prob]
def classify(data_dir, image_filenames):
    files = image_filenames
    dict_predictions = {}

    command = 'python guess.py --class_type gender --model_type inception --model_dir ./inception/21936/ --filename ' + './' + data_dir + '/'
    num_files = len(files)
    for filename in files:
        new_command = command + filename
        result = subprocess.run(new_command.split(), stdout=subprocess.PIPE)
        
        output = result.stdout.decode('utf-8')
        
        dict_predictions[filename] = parse_classifier_output(output)
        print("Done with " + filename)
        index = files.index(filename)
        print("done with " + str(index) + " out of " + str(num_files))

    print ("FINISHED with this many files: ")
    print (len(dict_predictions.keys()))
    return dict_predictions

# parse output (for part that starts with Guess), return predicted label, predicted prob
# output is of form: Guess @ 1 F, prob = 0.82
def parse_classifier_output(output):
     # parse the string outputted by stdout for Guess @ 1
    start_of_pred = "Guess @ 1"
    index_prediction = output.find(start_of_pred)
    # prediction string (Guess @ 1 F, prob = 0.82) has length 24, so slice string
    prediction_string = output[index_prediction:index_prediction+25]
    print("PREDICTED STRING")
    print(prediction_string)
    predicted_label = prediction_string[10]
    print("PREDICTED LABEL")
    print(predicted_label)
    predicted_prob = prediction_string[len(prediction_string)-5:len(prediction_string)]
    print("PREDICTED PROB")
    print(predicted_prob)

    return [predicted_label, predicted_prob]


# takes original csv with labels and dictionary of preedictions as inputs
# creates a new csv with predicted label, predicted prob, truee/false value
def create_csv_output(input_csv, dict_predictions):
    with open(input_csv,'r') as csvinput:
        with open("./predictions.csv", 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            header = next(reader)
            header.append('predicted_label')
            header.append('predicted_prob')
            all.append(header)

            dict_filenames = dict_predictions.keys()
            for row in reader:
                filename = row[0]
                predicted_label = ""
                predicted_prob = ""
                if filename in dict_filenames:
                    predicted_label = dict_predictions[filename][0]
                    predicted_prob = dict_predictions[filename][1]
                row.append(predicted_label)
                row.append(predicted_prob)
                all.append(row)

            writer.writerows(all)



# takes folder structure of images and creates dict with relavent features
def create_dict_from_dir_structure(top_level_dir):
    # folder structure under top_level_dir (top_level_dir needs to have / at end) is: gender (male or female) --> races --> cropped or orginal
    labels_dict = {}
    images = os.listdir(top_level_dir)
    for image in images:
        print("Working on image: " + image)
        attributes = image.split("_")

        gender = attributes[0]
        # print("GENDER")
        # print(gender)

        generated = False
        if "cropped" in image:
            generated = True
        # print("GENERATED")
        # print(generated)

        race = ""
        one_word_races = ["black", "indian", "white"]
        if attributes[2] in one_word_races:
            race = attributes[2]
        else:
            race = attributes[2] + " " + attributes[3]
        # print("RACE")
        # print(race)

        labels_dict[image] = {
            "filename": image,
            "gender": gender,
            "generated": generated,
            "race": race,
        }

    return labels_dict


# takes dictionary and writes it to a csv with columns filename, gender, race, generated (True/false)
def dict_to_annotations_csv(labels_dict):
    filename = "./annotations.csv"
    with open(filename, "w") as infile:
        writer = csv.DictWriter(infile, fieldnames=labels_dict["male_male_southeast_asian_original_43954.jpg"].keys())
        writer.writeheader()
        for image in labels_dict.keys():
            writer.writerow(labels_dict[image])


# calculate ppv for generated and original subsets of images
def ppvGenerated(predictions_csv):
    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)
        generated_count = 0
        original_count = 0
        total_generated_count = 0
        total_original_count = 0

        header = next(reader)

        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            generated = row[2]
            if (generated == "False"):
                total_original_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    original_count += 1
            else:
                total_generated_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    generated_count += 1
                
        print(total_generated_count + total_original_count)
        print(original_count)
        print(original_count/total_original_count * 100)
        print(generated_count/total_generated_count * 100)

# calculate ppv for race subsets
def ppvRaces(predictions_csv):
    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)

        white_count = 0
        total_white_count = 0

        black_count = 0
        total_black_count = 0

        me_count = 0
        total_me_count = 0

        indian_count = 0
        total_indian_count = 0

        se_count = 0
        total_se_count = 0

        ea_count = 0
        total_ea_count = 0

        lh_count = 0
        toal_lh_count = 0

        header = next(reader)

        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            race = row[3]
            if (race == "white"):
                total_white_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    white_count += 1
                    
            elif (race == "black"):
                total_black_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    black_count += 1

            elif (race == "middle eastern"):
                total_me_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    me_count += 1

            elif (race == "indian"):
                total_indian_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    indian_count += 1
                    
            elif (race == "southeast asian"):
                total_se_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    se_count += 1

            elif (race == "east asian"):
                total_ea_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    ea_count += 1

            elif (race == "latino hispanic"):
                toal_lh_count += 1
                if (actual_gender == "female" and predicted_gender == "F") or (actual_gender == "male" and predicted_gender == "M"):
                    lh_count += 1
                
        print(total_black_count + toal_lh_count + total_ea_count + total_indian_count + total_me_count + total_se_count + total_white_count)
        
        print(white_count/total_white_count * 100)
        print(black_count/total_black_count * 100)
        print(me_count/total_me_count * 100)
        print(indian_count/total_indian_count *100)
        print(se_count/total_se_count * 100)
        print(ea_count/total_ea_count * 100)
        print(lh_count/toal_lh_count * 100)

# calculate ppv for all images classified
def ppvAll(predictions_csv):
    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)
        count = 0
        total_count = 0
        header = next(reader)
        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            if (actual_gender == "female" and predicted_gender == "F"):
                count +=1
            elif (actual_gender == "male" and predicted_gender == "M"):
                count +=1
            
            total_count += 1

# calculate ppv for gender subsets
def ppvGenders(predictions_csv):

    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)
        female_count = 0
        male_count = 0
        total_male_count = 0
        total_female_count = 0
        header = next(reader)
        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            if actual_gender == 'female':
                total_female_count += 1
                if predicted_gender == "F":
                    female_count += 1
            elif actual_gender == 'male':
                total_male_count += 1
                if predicted_gender == "M":
                    male_count += 1
     
        print (total_male_count + total_female_count)
        print(female_count)
        print("FEMALES")
        print(total_female_count)
        print(female_count/total_female_count * 100)
        print("MALES")
        print(male_count)
        print(total_male_count)
        print(male_count/total_male_count * 100)

# calculate ppv for female/race subsets
def ppvRacesFemales(predictions_csv):
    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)

        white_count = 0
        total_white_count = 0

        black_count = 0
        total_black_count = 0

        me_count = 0
        total_me_count = 0

        indian_count = 0
        total_indian_count = 0

        se_count = 0
        total_se_count = 0

        ea_count = 0
        total_ea_count = 0

        lh_count = 0
        toal_lh_count = 0

        header = next(reader)

        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            race = row[3]
            if ((race == "white") and (actual_gender == "female")):
                total_white_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    white_count += 1
                    
            elif ((race == "black") and (actual_gender == "female")):
                total_black_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    black_count += 1

            elif ((race == "middle eastern") and (actual_gender == "female")):
                total_me_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    me_count += 1

            elif ((race == "indian") and (actual_gender == "female")):
                total_indian_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    indian_count += 1
                    
            elif ((race == "southeast asian") and (actual_gender == "female")):
                total_se_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    se_count += 1

            elif ((race == "east asian") and (actual_gender == "female")):
                total_ea_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    ea_count += 1

            elif ((race == "latino hispanic") and (actual_gender == "female")):
                toal_lh_count += 1
                if (actual_gender == "female" and predicted_gender == "F"):
                    lh_count += 1
                
        print(total_black_count + toal_lh_count + total_ea_count + total_indian_count + total_me_count + total_se_count + total_white_count)
        
        print(white_count/total_white_count * 100)
        print(black_count/total_black_count * 100)
        print(me_count/total_me_count * 100)
        print(indian_count/total_indian_count *100)
        print(se_count/total_se_count * 100)
        print(ea_count/total_ea_count * 100)
        print(lh_count/toal_lh_count * 100)

# calculate ppv for male/race subsets
def ppvRacesMales(predictions_csv):
    with open(predictions_csv, 'r') as inp:
        reader = csv.reader(inp)

        white_count = 0
        total_white_count = 0

        black_count = 0
        total_black_count = 0

        me_count = 0
        total_me_count = 0

        indian_count = 0
        total_indian_count = 0

        se_count = 0
        total_se_count = 0

        ea_count = 0
        total_ea_count = 0

        lh_count = 0
        toal_lh_count = 0

        header = next(reader)

        for row in reader:
            actual_gender = row[1]
            predicted_gender = row[4]
            race = row[3]
            if ((race == "white") and (actual_gender == "male")):
                total_white_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    white_count += 1
                    
            elif ((race == "black") and (actual_gender == "male")):
                total_black_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    black_count += 1

            elif ((race == "middle eastern") and (actual_gender == "male")):
                total_me_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    me_count += 1

            elif ((race == "indian") and (actual_gender == "male")):
                total_indian_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    indian_count += 1
                    
            elif ((race == "southeast asian") and (actual_gender == "male")):
                total_se_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    se_count += 1

            elif ((race == "east asian") and (actual_gender == "male")):
                total_ea_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    ea_count += 1

            elif ((race == "latino hispanic") and (actual_gender == "male")):
                toal_lh_count += 1
                if (actual_gender == "male" and predicted_gender == "M"):
                    lh_count += 1
                
        print(total_black_count + toal_lh_count + total_ea_count + total_indian_count + total_me_count + total_se_count + total_white_count)
        
        print(white_count/total_white_count * 100)
        print(black_count/total_black_count * 100)
        print(me_count/total_me_count * 100)
        print(indian_count/total_indian_count *100)
        print(se_count/total_se_count * 100)
        print(ea_count/total_ea_count * 100)
        print(lh_count/toal_lh_count * 100)



def main():
    # run classifier
    data_dir = "./data/"
    labels_csv = "./annotations.csv"
    image_filenames_to_classify = get_image_files(data_dir)
    create_empty_predictions_file('./annotations.csv')
    classify_and_record(data_dir, image_filenames_to_classify)
    
    # commands used to read in entire data set (from data-flat) and create annotations csv
    # dict_labelled = create_dict_from_dir_structure("./data/")
    # dict_to_annotations_csv(dict_labelled)

    # sample command to calculate stats
    ppvRacesMalesOriginal("./predictions_all.csv")



if __name__ == '__main__':
    main()





