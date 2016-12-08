# RefMat-Symlink

Use symlinks as tags to organize file archive (Reference Material).

Current version works for Windows OS (It was not tested on other OS)


## Folder structure for file archive

### Initial structure

```
-> ~/refdb/
    -> Inbox/
    -> Repository/
    -> Tags
        ->
```


 - Inbox - the app imports file from this folder only.
 - Repository - contains imported files in chronically order.
 - Tags - contains symlink

### Ready for impoting

```
-> ~/refdb/
    -> Inbox/
        -> sell_enverything
    -> Repository/
    -> Tags
```

 - Inbox/sell_everything - folder ready to import in RefMat-Symlink app.


### After importing sell_everyting project with tags *Client/TopSeller* and *Projects*
```
-> ~/refdb/
    -> Inbox/
    -> Repository/
        -> 201612/
            -> 01/
                -> sell_everything
    -> Tags
        -> Clients/
            -> TopSeller/
                -> @sell_everyhing
        -> Projects/
            -> @sell_everyting
```


 - Repository/201612/01/sell_everything - is real folder.
 - Tags/Clients/TopSeller/@sell_everthing and Tags/Projects/@sell_everything are symlinks to *sell_everthing* archive

## How to use:

### Initialize

```
python refmat_symlink/main.py initialize 
```

Create folder structure to keep file archives (in folder ~/refmatdb by default).

### Import

```
python refmat_symlink/main.py import Clients/TopSeller Projects
```

Import all files from Inbox folder and assign to them *Clients/TopSeller* and *Projects* tag.


