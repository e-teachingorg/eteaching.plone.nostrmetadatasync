# eteaching.plone.nostrmetadatasync

Nostr integration for Plone 6.

eteaching.plone.nostrmetadatasync synchronises metadata of Plone contents
with Nostr. This is done on the basis of subscribers (event handlers). When
content is created, deleted or modified on the Plone website, corresponding
Nostr events are created, signed and sent to predefined relias in the Nostr
network. Two control panels are also provided. One is for settings, where
you can specify which content types and filters should be used to select
the content affected by synchronization. The second control panel can be
used to create all events in the Nostre relays for the entire content
selected using the settings, or to send delete events.

## Features

* Real-time synchronization between metadata for event-based plone objects (e.g. plone.app.event) and Nostr time-based calendar events (NIP-52).
* Real-time synchronization between metadata for educational materials and Nostr AMB events (NIP-AMB)
* Initial creation of Nostr events for the metadata of all supported objects.
* Specific configuration options where portal types and additional restrictions for synchronization can be selected

## Installation

### Prerequisites ✅

-   An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned.
-	Python 3.10, 3.11, 3.12, or 3.13
-   [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
-   [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
-   [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)

### Install eteaching.plone.nostrmetadatasync from source with `git` 🔧

This is not an installation for production use, but rather for testing and development purposes.

1.  Clone this repository, then change your working directory

    ```shell
    git clone git@github.com:e-teachingorg/eteaching.plone.nostrmetadatasync.git
    cd eteaching.plone.nostrmetadatasync
    ```

2. Create environment and install uv

    ```shell
    python3 -m venv .
    bin/pip install uv
    source bin/activate
    ```
3. Create an .env file

    ```shell
    vi .env
    ```

	to set NOST_KEY as an environment variable:

    ```shell
    NOSTR_KEY=MyPrivateNostrKey
    ```

4.  Install the code base

    ```shell
    make install
    ```

5.	Create a empty Plone site (user:admin, password:admin)

	```shell
	make create-site
	```

6.	Start

	```shell
	make start
	```

### Install eteaching.plone.nostrmetadatasync via `buildout`

1. Use zc.buildout >=5, e.g. using the following requirements.txt:

	```shell
	horse-with-no-namespace==20251105.1
	packaging==25.0
	pip==25.3
	setuptools==80.9.0
	wheel==0.45.1
	zc.buildout==5.1.1
	```

2. Install Python venv and requirements:

	```shell
	bin/python3 -m venv .
	bin/pip install -r requirements.txt
	```

3. Create an .env file

    ```shell
    vi .env
    ```

	to set NOST_KEY as an environment variable:

    ```shell
    NOSTR_KEY=MyPrivateNostrKey
    ```

4. Add the following to buildout.cfg:

	```shell
	[buildout]

	eggs =
	    eteaching.plone.nostrmetadatasync
	...

	[instance]

	environment-vars =
		NOSTR_KEY ${env:NOSTR_KEY}
	...
	```

5. Run buildout

	```shell
	bin/buildout
	```
6. Start

	```shell
	bin/instance fg
	```

### Example: Set up synchronization for Plone News Items


1. Open your Plone site (e.g. http://localhost:8080/Plone for testing) in your browser

2. Login

3. Click "admin" ➔ "Site Setup"

4. Under "Add-ons", check to see if the "Nostr Metadata Sync" add-on is installed. If not, install it.

5. Then go back to "Site Setup" ➔ "Add-on Configuration" ➔ "Nostr Metadata Sync management"

7. Click "Configure this add-on"

8. Enter nostr relays. (If you've started Nak with `nak serve` on the same computer, enter the following: ws://localhost:10547)

9. Enable "News Item" under "Calendar adapter types"

10. You can enter additional search filters and also specify a community key if you want to sync to a specific community

11. Click "Save"

Now, when you create News Items in the portal and publish them, they should sync with the relays you've entered.




## Contribute

- [Issue tracker](https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync/issues)
- [Source code](https://github.com/e-teachingorg/eteaching.plone.nostrmetadatasync/)


## License

The project is licensed under the GPLv2.
