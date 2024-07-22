# 🫣rumpshaker

![image](images/rumpshaker.png)


Rumpshaker uses the python [rumps](https://github.com/jaredks/rumps) library to create a menubar that keeps track of common programming bookmarks like "TODO, FIXME, NOTE", etc.  
It also will track any emoji usage that it finds.

Rumpshaker was written entirely using a local LLM called [CodeLlama 70B](https://huggingface.co/codellama/CodeLlama-70b-hf).


install it with:

```
$> pip install .
```

start it with :

```
$>rumpshaker --directory ~/notes --file_types md txt

```

## Configuration

rumpshaker accepts a directory pattern that it will scan.  It also requires
filetypes that it will search for emojis and tags.
