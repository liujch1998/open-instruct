import transformers

# pm = transformers.LlamaForCausalLM.from_pretrained("allenai/tulu-v2.5-ppo-13b-uf-mean")
vm = transformers.LlamaForTokenClassification.from_pretrained("allenai/tulu-v2.5-ppo-13b-uf-mean-13b-uf-rm-value")