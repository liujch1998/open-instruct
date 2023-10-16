import copy
import subprocess
import yaml
import random
import re
import itertools
from datetime import date

today = date.today().strftime("%m%d%Y")

with open("beaker_configs/default_eval.yaml", 'r') as f:
    default_yaml = f.read()
d1 = yaml.load(default_yaml, Loader=yaml.FullLoader)

# cluster = "ai2/general-cirrascale"
cluster = "ai2/allennlp-cirrascale"
# cluster = "ai2/general-cirrascale-a100-80g-ib"
# cluster = "ai2/prior-elanding"
num_gpus = 1
d1['tasks'][0]['context']['cluster'] = cluster
d1['tasks'][0]['context']['priority'] = "high"
# d1['tasks'][0]['context']['priority'] = "preemptible"
d1['tasks'][0]['resources']['gpuCount'] = num_gpus

# modify here for different set of experiments
experiment_groups = [
    "mmlu_0shot",
    "mmlu_5shot",
    "gsm_direct",
    "gsm_cot",
    "bbh_direct",
    "bbh_cot",
    "tydiqa_goldp_1shot",
    "tydiqa_no_context_1shot",
    "codex_eval_temp_0.1",
    "codex_eval_temp_0.8",
    "trutufulqa",
    "toxigen",
    "alpaca_farm",
]

# model to evaluate, each in the followng format: model name, their beaker id, checkpoint subfolder
models = [
    # llama1 models
    # ("llama1-7B", "01HCCBK1MYKXKQC0C6CSVW1F22", None, "vanilla_lm"),
    # ("llama1-13B", "01HCCBWB4TWNS35N9R35K47BH8", None, "vanilla_lm"),
    # ("llama1-30B", "01HCCC7FNXFCQ2TFWGS2HA683Y", None, "vanilla_lm"),
    # ("llama1-65B", "01HCCCWQTPKS23W7MRFH5PXNHA", None, "vanilla_lm"),
    
    # llama2 models
    # ("llama2-7B", "01HCJYBBWA629B8GJTHPT496TT", None, "vanilla_lm"),
    # ("llama2-13B", "01HCJZQBM2KGQZSZRPF4HKVBZX", None, "vanilla_lm"),
    # ("llama2-70B", "01HCK281AFAXV2Y7T54NMNSC55", None, "vanilla_lm"),
    # ("llama2-chat-7B", "01HCT5D48MSRF0PCNAWNSJDN54", None, "tuned_lm"),
    # ("llama2-chat-13B", "01HCT5Q7A6FE8RZKY8TYN64ZW2", None, "tuned_lm"),
    # ("llama2-chat-70B", "01HCT63DVK7YPT6P9SN35XH417", None, "tuned_lm"),
    
    # our ablation models
    # ("finetuned_llama1_7B_dolly", "01GZVKGQZAMQMVG9307KWS4GMN", None, "tuned_lm"),
    # ("finetuned_llama1_7B_flan_v2", "01GZVKGR5DW1SXXWSMWE2QYWYR", None, "tuned_lm"),
    # ("finetuned_llama1_7B_cot", "01GZVKGRA3X4SYQF1PZ29DSZFE", None, "tuned_lm"),
    # ("finetuned_llama1_7B_code_alpaca", "01GZVKGREPDJ6FZM3S4B0J8VB9", None, "tuned_lm"),
    # ("finetuned_llama1_7B_baize", "01GZVKGRKAHJW2AK3ZF88G13HA", None, "tuned_lm"),
    # ("finetuned_llama1_7B_oasst1", "01GZVKGRQZ4359W31CAEHWFVSB", None, "tuned_lm"),
    # ("finetuned_llama1_7B_gpt4_alpaca", "01GZVKGRWJ2VVCXY5KP46814JP", None, "tuned_lm"),
    # ("finetuned_llama1_7B_super_ni", "01GZVKGS1S527GYKRA4Y26ZP5S", None, "tuned_lm"),
    # ("finetuned_llama1_7B_self_instruct", "01GZVKGS7JTYK0M35AFXHY0CD0", None, "tuned_lm"),
    # ("finetuned_llama1_7B_stanford_alpaca", "01GZVKGSHNPRFSJBS4K74FTRDC", None, "tuned_lm"),
    # ("finetuned_llama1_7B_unnatural_instructions", "01GZVKGSP9BAW8XTWB9509SPDB", None, "tuned_lm"),
    # ("finetuned_llama1_7B_sharegpt", "01GZWDNED8KP28SAR1159WZ366", None, "tuned_lm"),
    
    # ("finetuned_llama1_13B_oasst1", "01GZWN5FRTGJKEZR890MQRXZZ9", None, "tuned_lm"),
    # ("finetuned_llama1_13B_dolly", "01GZWN5FXP2ZEKJ8HBBWHK58TZ", None, "tuned_lm"),
    # ("finetuned_llama1_13B_super_ni", "01GZWN5G71CT6GFC9VC6T6RT5V", None, "tuned_lm"),
    # ("finetuned_llama1_13B_self_instruct", "01H0JSB1QDQDYPEG8AX127XMND", None, "tuned_lm"),
    # ("finetuned_llama1_13B_flan_v2", "01H04RBP7F545WC5APZK5DE58T", None, "tuned_lm"),
    # ("finetuned_llama1_13B_sharegpt", "01GZWN5G2DVDTSM508CW34V1FT", None, "tuned_lm"),
    # ("finetuned_llama1_13B_cot_lumi", "01H0F09XR3PNABMPD7X95PSR8H", None, "tuned_lm"),
    # ("finetuned_llama1_13B_baize_lumi", "01H0F123TJG9BXZ9WT42XTSDPS", None, "tuned_lm"),
    # ("finetuned_llama1_13B_code_alpaca_lumi", "01H0F1SF5WX84RXWJYZFS4CBW5", None, "tuned_lm"),
    # ("finetuned_llama1_13B_gpt4_alpaca_lumi", "01H0F43FKA2J7YY8N3K9A0CHFD", None, "tuned_lm"),
    # ("finetuned_llama1_13B_stanford_alpaca_lumi", "01H0F4TWK7YNB2YRK1TG5JEXZ5", None, "tuned_lm"),
    # ("finetuned_llama1_13B_unnatural_instructions_lumi", "01H0F5JTDM9WMKSPDBYH141089", None, "tuned_lm"),

    # ("finetuned_llama1_7B_flanv2_cot_oasst1_dolly_lumi", "01H0K4049XMFGD8PW7BB6KVGBZ", None, "tuned_lm"),
    # ("finetuned_llama1_13B_flanv2_cot_oasst1_dolly_lumi", "01H0KJ3ZFCDBGGV4FGS8RZXCXA", None, "tuned_lm"),
    # ("finetuned_llama1_30B_flanv2_cot_oasst1_dolly_lumi", "01H0NF25QSBTVDWYV7JJNKDYCV", None, "tuned_lm"),
    # ("finetuned_llama1_65B_flanv2_cot_oasst1_dolly_lumi", "01H0P3BKSC389DSK8KBPXW8JDF", None, "tuned_lm"),
    
    # tulu v1 models
    # ("tulu_v1_7B", "01H0K6A8P9TC25F5D0NMN8NTG7", None, "tuned_lm"),
    # ("tulu_v1_13B", "01H0JW5D7ETX8252T2AHKN6S94", None, "tuned_lm"),
    # ("tulu_v1_30B", "01H0PHQSWP1CYHBYF4EG8ABX3E", None, "tuned_lm"),
    # ("tulu_v1_65B", "01H0MHPS7Y3YTND66KCP16E4AC", None, "tuned_lm"),

    # tulu v2 ablation models
    # ("finetuned_llama2_7B_on_v1_data", "01H7ABFYB84N9TN8MYXAVSMJ68", None, "tuned_lm"),
    # ("finetuned_llama2_13B_on_v1_data", "01H7AC0KXGRDH9ACJ24WTSK7SR", None, "tuned_lm"),
    # ("finetuned_llama2_7B_on_v1_data_qlora", "", None, "tuned_lm"),
    # ("finetuned_llama2_13B_on_v1_data_qlora", "", None, "tuned_lm"),

    # tulu v2 models
    # ("tulu_v2_7B_qlora", "01HC68D92TWTWBX55EY4N22P0N", None, "tuned_lm"),
    # ("tulu_v2_13B_qlora", "01HC8HN28F7XH3RWYZX6J1PFRJ", None, "tuned_lm"),
    # ("tulu_v2_70B_qlora", "01HC80Q3GTSGW4B5HZSDC7TT2K", None, "tuned_lm"),
    # ("tulu_v2_7B_jax", "01HBXTF305QARZ7P4T6ASXXVAM", None, "tuned_lm"),
    # ("tulu_v2_13B_jax", "01HBWE5NHC3M30HH63339HS8BE", None, "tuned_lm"),
    # ("tulu_v2_70B_jax", "01HCB2VZJ2T2JXZX0R1SJBRSB2", None, "tuned_lm"),

    # other causal models
    # ("hf-opt-7B", "facebook/opt-6.7b", None, "vanilla_lm"),
    # ("finetuned_opt_7B_flanv2_cot_oasst1_dolly_sharegpt_gpt4alpaca_codealpaca_lumi", "01H13EBXSADXXJCRERART90ZKJ", None, "tuned_lm"),
    # ("hf-pythia-7B", "EleutherAI/pythia-6.9b", None, "vanilla_lm"),
    # ("fintuned_pythia_7B_flanv2_cot_oasst1_dolly_sharegpt_gpt4alpaca_codealpaca_lumi", "01H1359QTQZCXFTW4KY4WVKF0C", None, "tuned_lm"),
    # ("hf-falcon-40B", "tiiuae/falcon-40b", None, "vanilla_lm"),
    # ("finetuned_falcon_40B_flanv2_cot_oasst1_dolly_sharegpt_gpt4alpaca_codealpaca_lumi", "01H2TRXD9TE80W61PABE26785P", None, "tuned_lm"),
    # ("hf-falcon-7B", "tiiuae/falcon-7b", None, "vanilla_lm"),
    # ("finetuned_falcon_7B_flanv2_cot_oasst1_dolly_sharegpt_gpt4alpaca_codealpaca_lumi", "01H356X9ZYY8HX1C7HFH6JYWNW", None, "tuned_lm"),
    # ("hf-falcon-rw-7B", "tiiuae/falcon-rw-7b", None, "vanilla_lm"),
    # ("finetuned_falcon_rw_7B_flanv2_cot_oasst1_dolly_sharegpt_gpt4alpaca_codealpaca_lumi", "01H37QXWFK095588W6GCMVGFKB", None, "tuned_lm"),

]

#--------------- experiments about number of supervision tasks -------------------------

# for experiment_group, model_info in itertools.product(experiment_groups, models):
for model_info, experiment_group in itertools.product(models, experiment_groups):
    print(f"Submitting {experiment_group} for model: {model_info[0]}")
    d = copy.deepcopy(d1)

    model_name = model_info[0] + f"_{model_info[2]}" if model_info[2] is not None else model_info[0]
    name = f"open_instruct_eval_{experiment_group}_{model_name}_{today}"
    d['description'] = name
    d['tasks'][0]['name'] = name

    if experiment_group == "mmlu_0shot":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.mmlu.run_eval \
            --ntrain 0 \
            --data_dir /data/mmlu/ \
            --save_dir /output/ \
            --model_name_or_path /model \
            --tokenizer_name_or_path /model \
            --eval_batch_size 4 \
            --load_in_8bit \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "mmlu_5shot":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.mmlu.run_eval \
            --ntrain 5 \
            --data_dir /data/mmlu/ \
            --save_dir /output/ \
            --model_name_or_path /model \
            --tokenizer_name_or_path /model \
            --eval_batch_size 4 \
            --load_in_8bit \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "bbh_direct":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.bbh.run_eval \
            --data_dir /data/bbh \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --max_num_examples_per_task 40 \
            --no_cot \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "bbh_cot":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.bbh.run_eval \
            --data_dir /data/bbh \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --max_num_examples_per_task 40 \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "gsm_direct":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.gsm.run_eval \
            --data_dir /data/gsm/ \
            --max_num_examples 200 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --n_shot 8 \
            --no_cot \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "gsm_cot":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.gsm.run_eval \
            --data_dir /data/gsm/ \
            --max_num_examples 200 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --n_shot 8 \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        ''' 
    elif experiment_group == "tydiqa_goldp_1shot":
        d["tasks"][0]["arguments"][0] = '''
            python -m eval.tydiqa.run_eval \
            --data_dir /data/tydiqa/ \
            --n_shot 1 \
            --max_num_examples_per_lang 100 \
            --max_context_length 512 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "tydiqa_no_context_1shot":
        d["tasks"][0]["arguments"][0] = '''
            python -m eval.tydiqa.run_eval \
            --data_dir /data/tydiqa/ \
            --no_context \
            --n_shot 1 \
            --max_num_examples_per_lang 100 \
            --max_context_length 512 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "codex_eval_temp_0.1":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.codex_humaneval.run_eval \
            --data_file /data/codex_humaneval/HumanEval.jsonl.gz \
            --eval_pass_at_ks 1 5 10 20 \
            --unbiased_sampling_size_n 20 \
            --temperature 0.1 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model
        '''
    elif experiment_group == "codex_eval_temp_0.8":
        d['tasks'][0]['arguments'][0] = '''
            python -m eval.codex_humaneval.run_eval \
            --data_file /data/codex_humaneval/HumanEval.jsonl.gz \
            --eval_pass_at_ks 1 5 10 20 \
            --unbiased_sampling_size_n 20 \
            --temperature 0.8 \
            --save_dir /output/ \
            --use_vllm \
            --model /model \
            --tokenizer_name_or_path /model
        '''
    elif experiment_group == "trutufulqa":
        d['tasks'][0]['arguments'][0] = '''
        python -m eval.truthfulqa.run_eval \
            --data_dir /data/truthfulqa \
            --save_dir /output/ \
            --model_name_or_path /model \
            --tokenizer_name_or_path /model \
            --metrics judge info mc \
            --preset qa \
            --gpt_judge_model_name curie:ft-allennlp:gpt-judge-2023-07-26-09-37-48 \
            --gpt_info_model_name curie:ft-allennlp:gpt-info-2023-07-26-11-38-18 \
            --eval_batch_size 20 \
            --load_in_8bit \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "toxigen":
        d['tasks'][0]['arguments'][0] = '''
        python -m eval.toxigen.run_eval \
            --data_dir /data/toxigen/ \
            --save_dir /output/ \
            --model_name_or_path /model \
            --tokenizer_name_or_path /model \
            --eval_batch_size 32 \
            --use_vllm \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    elif experiment_group == "alpaca_farm":
        d['tasks'][0]['arguments'][0] = '''
        python -m eval.alpaca_farm.run_eval \
            --use_vllm \
            --model_name_or_path /model \
            --tokenizer_name_or_path /model \
            --save_dir /output/ \
            --use_chat_format \
            --chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format
        '''
    else:
        raise ValueError("experiment_group not supported")

    # if a specific checkpoint is specified, load model from that checkpoint
    if model_info[2] is not None:
        assert "--model_name_or_path /model" in d['tasks'][0]['arguments'][0]
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--model_name_or_path /model", "--model_name_or_path /model/"+model_info[2])]
        assert "--tokenizer_name_or_path /model" in d['tasks'][0]['arguments'][0]
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--tokenizer_name_or_path /model", "--tokenizer_name_or_path /model/"+model_info[2])]

    # for vanilla_lm, remove the chat formatting function
    if model_info[3] == "vanilla_lm":
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--use_chat_format", "")]

    if "13B" in model_info[0]:
        # find the batch size argument, and reduce by 4x
        if "--eval_batch_size" in d['tasks'][0]['arguments'][0]:
            original_batch_size = re.search("--eval_batch_size (\d+)", d['tasks'][0]['arguments'][0]).group(1)
            new_batch_size = max(1, int(original_batch_size) // 2)
            d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--eval_batch_size {}".format(original_batch_size), "--eval_batch_size {}".format(new_batch_size))]


    if "30B" in model_info[0]:
        # find the batch size argument, and reduce by 4x
        if "--eval_batch_size" in d['tasks'][0]['arguments'][0]:
            original_batch_size = re.search("--eval_batch_size (\d+)", d['tasks'][0]['arguments'][0]).group(1)
            new_batch_size = max(1, int(original_batch_size) // 4)
            d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--eval_batch_size {}".format(original_batch_size), "--eval_batch_size {}".format(new_batch_size))]

        if "codex_eval" in experiment_group:
            # request 2x more GPUs
            d['tasks'][0]['resources']['gpuCount'] = 2 * d['tasks'][0]['resources']['gpuCount']
    
    elif "70B" in model_info[0] or "65B" in model_info[0] or "40B" in model_info[0]:
        # find the batch size argument, and reduce by 4x
        if "--eval_batch_size" in d['tasks'][0]['arguments'][0]:
            original_batch_size = re.search("--eval_batch_size (\d+)", d['tasks'][0]['arguments'][0]).group(1)
            new_batch_size = max(1, int(original_batch_size) // 4)
            d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--eval_batch_size {}".format(original_batch_size), "--eval_batch_size {}".format(new_batch_size))]

        if "codex_eval" in experiment_group:
            # request 4x more GPUs
            d['tasks'][0]['resources']['gpuCount'] = 4 * d['tasks'][0]['resources']['gpuCount']
        else:
            # request 2x more GPUs
            d['tasks'][0]['resources']['gpuCount'] = 2 * d['tasks'][0]['resources']['gpuCount']

    if model_info[0].startswith("hf-"):  # if it's a huggingface model, load it from the model hub
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--use_chat_format", "")]
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--model_name_or_path /model", "--model_name_or_path "+model_info[1])]
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace("--tokenizer_name_or_path /model", "--model_name_or_path "+model_info[1])]
    else:  # if it's a beaker model, mount the beaker dataset to `/model`
        d['tasks'][0]['datasets'][1]['source']['beaker'] = model_info[1]

    if "llama2-chat" in model_info[0]:
        d['tasks'][0]['arguments'] = [d['tasks'][0]['arguments'][0].replace(
            "--chat_formatting_function eval.templates.create_prompt_with_tulu_chat_format", 
            "--chat_formatting_function eval.templates.create_prompt_with_llama2_chat_format")
        ]

    # print(d)

    fn = "beaker_configs/auto_created/{}.yaml".format(name)
    file = open(fn, "w")
    yaml.dump(d, file, default_flow_style=True)
    file.close()

    cmd = "beaker experiment create {} --workspace ai2/yizhong_default".format(fn)
    subprocess.Popen(cmd, shell=True)
