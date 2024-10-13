import { ChartConfiguration } from "chart.js";

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

export interface QueueTrackObject extends TrackObject {
	queue_type: "queue" | "next_up";
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

	progress_ms: number;
	is_playing: boolean;

	repeat_state: "off" | "track" | "context";
	shuffle_state: boolean;

	currently_playing_type: "track" | "episode" | "ad" | "unknown";

}

export interface SpotifyQueue {
	currently_playing: TrackObject | null;
	queue: QueueTrackObject[];
}

export interface UserData {
	id: number;
	discord_user_id: number;

	discord_display_name: string;
}

export function millisecondsToTimeString(ms: number): string {
	const minutes = Math.floor(ms / 60000);
	const seconds = Math.floor((ms % 60000) / 1000);

	if (seconds < 10)
		return `${ minutes }:0${ seconds }`;
	else
		return `${ minutes }:${ seconds }`;
}

export interface DbArtist {
	spotify_name: string;
	spotify_id: string;

	spotify_large_image_link: string;
	spotify_small_image_link: string;
}

export interface DbSong {
	spotify_name: string;
	spotify_id: string;

	spotify_large_image_link: string;
	spotify_small_image_link: string;

	explicit: boolean;

	length_ms: number;
	spotify_artists: DbArtist[];
}


export interface ApiStats {
	total_requests: number;
	total_ms_listened: number;

	requests_grouped_by_date: {
		date: string;
		request_count: number;
	}[];

	most_requested_artists: {
		artist: DbArtist;

		request_count: number;
	}[];

	most_requested_songs: {
		song: DbSong;
		request_count: number;
	}[];
}


export interface ChartableApiStats extends ApiStats {
	request_grouped_by_date_chartable: ChartConfiguration["data"];
}


function isTrackObject(object: TrackObject | DbSong): object is TrackObject {
	return "album" in object;
}

function isSpotifySimplifiedArtistObject(object: SpotifySimplifiedArtistObject | DbArtist): object is SpotifySimplifiedArtistObject {
	return "external_urls" in object;
}

export interface CommonArtist {
	name: string;
	spotify_id: string;
}

export interface CommonSong {
	spotify_name: string;
	spotify_id: string;

	spotify_large_image_link: string;
	spotify_small_image_link: string;

	explicit: boolean;

	length_ms: number;
	spotify_artists: CommonArtist[];
}

export function toCommonArtist(artist: SpotifySimplifiedArtistObject | DbArtist): CommonArtist {
	if (isSpotifySimplifiedArtistObject(artist)) {
		return {
			name: artist.name,
			spotify_id: artist.id
		}

	} else {
		return {
			name: artist.spotify_name,
			spotify_id: artist.spotify_id,
		};
	}
}

export function toCommonSong(track: TrackObject | DbSong): CommonSong {
	if (isTrackObject(track)) {
		return {
			spotify_name: track.name,
			spotify_id: track.id,
			spotify_artists: track.artists.map(x => toCommonArtist(x)),
			explicit: track.explicit,
			length_ms: track.duration_ms,
			spotify_large_image_link: track.album.images.at(0)?.url!,
			spotify_small_image_link: track.album.images.at(track.album.images.length - 1)?.url!,
		}
	} else {
		return {
			explicit: track.explicit,
			length_ms: track.length_ms,
			spotify_artists: track.spotify_artists.map(x => toCommonArtist(x)),
			spotify_id: track.spotify_id,
			spotify_large_image_link: track.spotify_large_image_link,
			spotify_small_image_link: track.spotify_small_image_link,
			spotify_name: track.spotify_name
		};
	}
}
