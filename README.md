# Cực lẹ
"Cực lẹ" is a Vietnamese abverb, which means very fast! As its named, here is a quick-app for those who are too lazy to open up their photo editor.

For now it's just do some simple task like write text and make watermark

## Text
<table border="0">
 <tr>
    <td><img src='/uploads/sillycat.jpg' width='200'>
    <td><img src='/static/images/exports/sillycat.jpg' width='200'>
 </tr>
 <tr>
    <td>Before</td>
    <td>After</td>
 </tr>
</table>

Text can be add in 3 position: top, middle and bottom
<table border="0">
 <tr>
    <td><img src='/static/images/exports/whattt.jpg' width='400'>
 </tr>
 <tr>
    <td>Why it's like this?</td>
 </tr>
</table>

## Frame
Moreover use can add frame as a placeholder to your text

<table border="0">
 <tr>
    <td><img src='/static/images/exports/crying.jpg' width='125'>
    <td><img src='/static/images/exports/not so cool.jpg' width='125'>
    <td><img src='/static/images/exports/overexcited.jpg' width='150'>
 </tr>
 <tr>
    <td>Add</td>
    <td>Portfolio</td>
    <td>What?</td>
 </tr>
</table>

## Watermark
You can add watermark as text or image
<table border="0">
 <tr>
    <td><img src='/static/images/exports/sadcat-1.jpg' width='250'>
    <td><img src='/static/images/exports/sadcat-2.jpg' width='250'>
 </tr>
 <tr>
    <td>At conner</td>
    <td>Random</td>
 </tr>
 <tr>
    <td><img src='/static/images/exports/sadcat-3.jpg' width='250'>
    <td><img src='/static/images/exports/sadcat-4.jpg' width='250'>
 </tr>
 <tr>
    <td>Overlay</td>
    <td>Text</td>
 </tr>
</table>

## URL generate
There's another way to generate image much faster

By using URL with this format
```
https://cuc-le.onrender.com/edit/?img=https://www.example.com/&<attribute>=<value>
```

Example:
```
https://cuc-le.onrender.com/edit/?img=https://i.imgur.com/R9QlBVy.jpeg&bot=Hello-everyone
```

<table border="0">
 <tr>
    <td><img src='https://cuc-le.onrender.com/edit/?img=https://i.imgur.com/R9QlBVy.jpeg&bot=Hello-everyone' width='400'>
 </tr>
</table>
 

For `?img=` is your URL image, which required

After that is a `&` syntax, which is connect your attribute. And a `=` is there attribute value

### Attributes

#### Text position
  
| Syntax | Description                        |
|--------|------------------------------------|
|`top`   | Write text from top of the image   |
|`mid`   | Write text from middle of the image|
|`bot`   | Write text from bottom of the image|

```
https://cuc-le.onrender.com/edit/?img=https://i.imgur.com/R9QlBVy.jpeg&top=hello-everyone&mid=hahahahah&bot=~l3
```

You can see there are some syntax kinda diffrent, because url doesn't allow some special charactor

In URLs, spaces can be inserted using underscores or dashes:

- underscore (`_`) → space (` `)
- dash (`-`) → space (` `)
- 2 underscores (`__`) → underscore (`_`)
- 2 dashes (`--`) → dash (`-`)
- tilde + N (`~n`) → newline character

Reserved URL characters can be included using escape patterns:

- tilde + Q (`~q`) → question mark (`?`)
- tilde + A (`~a`) → ampersand (`&`)
- tilde + P (`~p`) → percentage (`%`)
- tilde + H (`~h`) → hashtag/pound (`#`)
- tilde + S (`~s`) → slash (`/`)
- tilde + B (`~b`) → backslash (`\`)
- tilde + L (`~l`) → less-than sign (`<`)
- tilde + G (`~g`) → greater-than sign (`>`)
- 2 single quotes (`''`) → double quote (`"`)
  
#### Frame
| Syntax | Description | Valid value              |
|--------|-------------|--------------------------|
|`fr`    | Add frame   |`add`, `portfolio`, `what`|

#### Watermark
| Syntax | Description                    | Valid value                                          |
|--------|--------------------------------|------------------------------------------------------|
|`wtk`   | Add watermark by URL           |image url                                             |
|`wtkt`  | Add watermark by custom text   |text                                                  |
|`wtkl`  | Custom layout of watermark     |`conner`, `ranning`, `overlay`                        |
|`wtkp`  | Custom position of watermark   |`bottom-left`, `bottom-right`, `top-left`, `top-right`|


## Tech Stack
- Python
- HTML
- CSS
- JavaScript
- Jinja
  
## Libraries Used
- PIL - For python image processing
- Flask - For using flask features and jinja templating
- pillow_heif - Adding support for heic and heif images
- flask_sessions - For web browser sessions
- Os - For data access
- Io - For open url to bitmap

# Installing
First, download repository and run some command below to install some necessary library:
 #### Create an environment
 ```
 $ python3 -m venv .venv
 ```
 #### Activate the environment
 ```
 $ .venv/bin/activate
 ```
 #### Installing flask
 ```
 $ pip install Flask
 ```
 #### Installing Pillow
 ```
 $ python3 -m pip install --upgrade Pillow
 ```

After install those library, start program by running command:
```
$ flask --app app --debug run
```
Your program will start running on `http://127.0.0.1:5000`

