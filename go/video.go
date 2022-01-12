package main

import (
	"log"
	"github.com/reiver/go-v4l2"
	"github.com/reiver/go-v4l2/framesize"
	)

func video() {
	if device, err := v4l2.Open(v4l2.Video0); nil != err {
		panic(err)
	} else {
		defer device.Close()
		log.Printf("Driver: %q\n", device.MustDriver())
		log.Printf("Card: %q\n", device.MustCard())
		log.Printf("BusInfo: %q\n", device.MustBusInfo())
		log.Printf("Version: %q\n", device.MustVersion())
		log.Printf("Has Video Capture: %v\n", device.MustHasCapability(v4l2.CapabilityVideoCapture))
		log.Printf("Has Streaming I/O: %v\n", device.MustHasCapability(v4l2.CapabilityStreaming))
		if formatFamilies, err := device.FormatFamilies(); nil != err {
			panic(err)
		} else {
			defer formatFamilies.Close()
			var formatFamily v4l2.FormatFamily
			for formatFamilies.Next() {
				if err := formatFamilies.Decode(&formatFamily); nil != err {
					panic(err)
				}
				log.Printf("\tformatFamily %q (%q) {compressed=%t} {emulated=%t}\n",
					formatFamily.Description(),
					formatFamily.PixelFormat(),
					formatFamily.HasFlags(v4l2.FormatFamilyFlagCompressed),
					formatFamily.HasFlags(v4l2.FormatFamilyFlagEmulated),
				)
			}
			if err := formatFamilies.Err(); nil != err {
				panic(err)
			}
			frameSizes, err := formatFamily.FrameSizes()
			if nil != err {
				panic(err)
			}
			defer frameSizes.Close()
			var frameSize v4l2_framesize.Type
			for frameSizes.Next() {
				if err := frameSizes.Decode(&frameSize); nil != err {
					panic(err)
				}
				casted, err := frameSize.Cast()
				if nil != err {
					panic(err)
				}
				switch t := casted.(type) {
				case v4l2_framesize.Discrete:
					log.Printf("\tframesizeDiscrete pixel_format=%q, width=%d, height=%d\n",
						t.PixelFormat,
						t.Width,
						t.Height,
					)
				case v4l2_framesize.Continuous:
					log.Printf("\tframesizeContinuous pixel_format=%q, min_width=%d, max_width=%d, min_height=%d, max_height=%\n",
						t.PixelFormat,
						t.MinWidth,
						t.MaxWidth,
						t.MinHeight,
						t.MaxHeight,
					)
				case v4l2_framesize.Stepwise:
					log.Printf("\tframesizeStepwise pixel_format=%q, min_width=%d, max_width=%d, min_height=%d, max_height=%\n",
						t.PixelFormat,
						t.MinWidth,
						t.MaxWidth,
						t.MinHeight,
						t.MaxHeight,
					)
				default:
					panic(err)
				}
			}
			if err := frameSizes.Err(); nil != err {
				panic(err)
			}
		}
	}
}
