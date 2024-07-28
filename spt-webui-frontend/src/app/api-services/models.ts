export interface SpotifySimplifiedArtistObject {
	href: string;
	id: string;
	uri: string;

	external_urls: {
		spotify: string;
	}

	name: string;
	type: "artist";
}

export interface SpotifyImageObject {
	url: string;
	width: number;
	height: number;
}

export interface TrackObject {
    id: string;

    duration_ms: number;
    name: string;
    popularity: number;
    explicit: boolean;

	artists: SpotifySimplifiedArtistObject[];

    external_urls: {
        spotify: string;
    }
    href: string;
    uri: string;

	album: {
		id: string;

		album_type: "album" | "single" | "compilation";
		total_tracks: number;

		external_urls: {
			spotify: string;
		}
		href: string;
		uri: string;

		images: SpotifyImageObject[];

		name: string;
		release_date: string;
		type: "album";
	}


    type: "track";


    is_local: boolean;
}

export interface SpotifyContextObject {
	type: "artist" | "playlist" | "album" | "show";
	href: string;
	uri: string;

	external_urls: {
		spotify: string;
	}
}

// non-complete
export interface PlaybackState {
	context: SpotifyContextObject;
	item: TrackObject;

	currently_playing_type: "track" | "episode" | "ad" | "unknown";

}

export interface SpotifyQueue {
	currently_playing: TrackObject;
	queue: TrackObject[];
}
