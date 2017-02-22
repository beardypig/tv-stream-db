# Live TV Stream DB

A database of live TV streams from around the world. 


## Data Files

The data files are located in the `datafiles` directory and are in JSON format, there will possibly be a number of sections for the data files, however, there is only `streams` at the moment.
 
In the `streams` data files there is one file per provider to aid in organisation.
 
The Files have the follow schema:

```js
{
    "name": providerName,                   /* (String) Required: Provider Name, usually the domain name; eg. raiplay.it */
    "attributes": {                         /* (Map) Optional: A set of default attributes for the streams */
        "geolocked": geoLocked,             /* (Boolean) Optional: If the stream is geolocked or not; Default=false */
        "region": region,                   /* (String) Optional: An ISO3116 alpha2 country code; eg. ES; Default=null */
        "language": language,               /* (String) Optional: An ISO639 alpha3 language code; eg. cat; Default=und */
        "authentication": authenticated,    /* (Boolean) Optional: If the streams require authentication; Default=false */
        "drm": DRM,                         /* (Boolean) Optional: If the stream is protected by DRM; Default=false */
        "hd": HD,                           /* (Boolean) Optional: If the stream is available in High Definition; Default=false*/
    },
    "streams": [                            /* (List) Required: A list of the streams available from the provider */
        {                                   /* (Map) Required, Repeated: Information about a stream */
            "name": streamName,             /* (String) Required: A "slug" style name, this must be unique in the set of streams; eg. bbcnews */
            "title": streamTitle,           /* (String) Required: The title of the stream, eg. BBC News */
            "url": streamURL,               /* (String) Required: The URL for the stream, eg. http://www.rtve.es/directo/la-1/ */
            "attributes": {}                /* (Map) Optional: Same as the top level attributes, but override for the current stream 
                                                For example, if geolocked is true in the top level attributes, but one 
                                                of the streams is not geolocked, then geolocked can be set here for that 
                                                particular stream */
        }
    ]
}
```

See `datafiles/streams/raiplay.json` for a complete example.

## Output

- HTML: [Browsable HTML Listing](https://beardypig.github.io/tv-stream-db/)
- TSV: tbd
- sqlite: tbd


## Related Projects
 
- [Streamlink](http://github.com/streamlink/streamlink) - recommended for playing most of the streams
