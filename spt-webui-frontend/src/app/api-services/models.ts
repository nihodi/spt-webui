export interface TrackObject {
    id: string;

    duration_ms: number;
    name: string;
    popularity: number;
    explicit: boolean;

    external_urls: {
        spotify: string;
    }
    href: string;
    uri: string;


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
