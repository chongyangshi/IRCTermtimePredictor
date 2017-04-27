file = fopen('messages_by_day.csv');
USER_COUNT = 10;
format = '%s';
for i = 1:USER_COUNT
    format = [format '%f'];
end
format = [format '%f']; % Target
data = textscan(file, format, 'Delimiter', ',', 'HeaderLines', 1);
inputs = [];
for i = 2:(USER_COUNT+2)
    inputs = [inputs; data{i}'];
end
scaled_inputs = mapminmax(inputs, 0, 1);

training_set = scaled_inputs(:, 1:2:end); %Odd rows
validation_set = scaled_inputs(:, 2:2:end); %Even rows

training_input = training_set(1:USER_COUNT,:);
training_target = training_set((USER_COUNT+1),:);
validation_input = validation_set(1:USER_COUNT,:);
validation_target = validation_set((USER_COUNT+1),:);

network_size = [USER_COUNT floor(USER_COUNT / 2) floor(USER_COUNT / 2)];

test_lm = feedforwardnet(network_size, 'trainlm');
[test_lm, test_lm_record] = train(test_lm, training_input, training_target);
fprintf('%s LM Training MSE: %f.\n', network_size, test_lm_record.best_perf);
result = test_lm(validation_input);
perf = perform(test_lm, validation_target, result);
fprintf('%s LM Validation MSE: %f.\n', network_size, perf);
fprintf('%s LM Validation Actual Misclassification Rate: %f.\n', network_size, get_misclassification(result, validation_target));