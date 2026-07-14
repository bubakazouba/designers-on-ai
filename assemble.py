# -*- coding: utf-8 -*-
"""Assemble the FINAL artists-only dataset for site #1 v2:
 - artists only (dropped CEOs/AI-execs/no-AI-work people)
 - AI-work images ONLY (no headshots)
 - every citation dated
Merges: keeper profiles (inline) + AI-work images + the 10 researched new AI artists.
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- 11 KEEPERS (established designers/artists with real AI work) ----
# credentials_date / quote_date from the dated-citations research pass.
KEEPERS = [
  {
    "name": "Refik Anadol", "domain": "Media Art / AI Data Art",
    "credentials": "Turkish-American media artist and pioneer of AI/data art; founder of Refik Anadol Studio (2014), former Google artist-in-residence, and creator of the solo AI installation 'Unsupervised' exhibited at the Museum of Modern Art (MoMA).",
    "credentials_source": "https://www.wipo.int/en/web/wipo-magazine/articles/painting-with-data-how-media-artist-refik-anadol-creates-art-using-generative-ai-67301",
    "credentials_date": "1 December 2024",
    "quote": "What happens if a machine can dream and, if it can, who defines what is real and what is not?",
    "quote_source": "https://www.wipo.int/en/web/wipo-magazine/articles/painting-with-data-how-media-artist-refik-anadol-creates-art-using-generative-ai-67301",
    "quote_date": "1 December 2024",
    "ai_work_images": [
      {"url": "https://static.designboom.com/wp-content/uploads/2022/11/refik-anadol-unsupervised-moma-designboom-full-width.jpg", "caption": "'Unsupervised' at MoMA - Anadol's ML model, trained on ~200 years of MoMA collection metadata, generating real-time AI visuals on a 24x24ft wall."},
      {"url": "https://static.designboom.com/wp-content/uploads/2022/11/refik-anadol-unsupervised-moma-designboom-03.jpg", "caption": "'Unsupervised - Machine Hallucinations: MoMA' - AI-generated morphing forms from Anadol's model interpreting the MoMA dataset."},
      {"url": "https://static.designboom.com/wp-content/uploads/2022/11/refik-anadol-unsupervised-moma-designboom-06.jpg", "caption": "Output view of Anadol's AI data-art installation 'Unsupervised' at MoMA."}
    ]
  },
  {
    "name": "Beeple (Mike Winkelmann)", "domain": "Digital Art",
    "credentials": "Digital artist behind 'Everydays: The First 5000 Days,' which sold at Christie's for $69.3 million in 2021; one of the most-followed digital artists working today. His 'Diffuse Control' is a genuine generative-AI installation (The Shed, then LACMA).",
    "credentials_source": "https://en.wikipedia.org/wiki/Beeple",
    "credentials_date": "n/a - living reference",
    "quote": "For those who have not checked it out yet @midjourney is pretty insane. Gonna be really interesting to see how these amazing new AI tools affect art moving forward when you can literally just type a few words and make something.",
    "quote_source": "https://x.com/beeple/status/1530354389109682177",
    "quote_date": "28 May 2022",
    "ai_work_images": [
      {"url": "https://unframed.lacma.org/sites/default/files/field/image/251027_Beeple_Image%202.png", "caption": "AI-generated output from Beeple's 'Diffuse Control' generative-AI sculpture (LACMA) - a real-time diffusion system transforming source images into new abstractions."},
      {"url": "https://unframed.lacma.org/sites/default/files/field/image/image2.png", "caption": "AI-generated abstraction from the 'Soft Jelly' iteration of Beeple's 'Diffuse Control' custom generative-AI sculpture."},
      {"url": "https://unframed.lacma.org/sites/default/files/attachments/iteration.png", "caption": "AI-generated iteration still from Beeple's 'Diffuse Control' installation, showing the human+machine image evolution."}
    ]
  },
  {
    "name": "Paul Trillo", "domain": "Film / Motion Direction",
    "credentials": "Award-winning director and visual artist whom OpenAI commissioned to create the first official Sora-generated music video (Washed Out's 'The Hardest Part'); a longtime experimental filmmaker known for inventive camera techniques.",
    "credentials_source": "https://www.forbes.com/sites/charliefink/2024/05/07/openais-sora-brings-directors-10-year-music-video-vision-to-life/",
    "credentials_date": "7 May 2024",
    "quote": "What is unique about AI is that it's this more fluid, organic process where you're ideating... That's what's been really exciting for me: you can actually spend more time trying to craft that story.",
    "quote_source": "https://www.forbes.com/sites/charliefink/2024/05/07/openais-sora-brings-directors-10-year-music-video-vision-to-life/",
    "quote_date": "7 May 2024",
    "ai_work_images": [
      {"url": "https://ars.electronica.art/hope/files/2024/08/wo_hardest_part_still_01.jpg", "caption": "Still from Washed Out 'The Hardest Part' - the first official OpenAI Sora-generated music video, directed by Paul Trillo (~700 clips generated, 55 used)."},
      {"url": "https://ars.electronica.art/hope/files/2024/08/wo_hardest_part_cover.jpg", "caption": "Cover frame from Trillo's Sora-generated Washed Out video - surreal dream-logic imagery unique to the Sora AI model."}
    ]
  },
  {
    "name": "Bradley G. Munkowitz (GMUNK)", "domain": "Motion Graphics / Design Direction",
    "credentials": "American motion-graphics design director and artist with 20+ years in the field; led the team that designed the holographic screen-graphics/UI for the sci-fi feature Tron: Legacy.",
    "credentials_source": "https://www.cgchannel.com/2011/11/qa-bradley-gmunk-munkowitz-design-director/",
    "credentials_date": "November 2011",
    "quote": "Until about a year ago, there was one way to achieve these types of effects. Now with AI and the power of the Z8 Fury, there are ten ways to do it, and the results are all incredible.",
    "quote_source": "https://www.thisiscolossal.com/2024/03/gmunk-hp/",
    "quote_date": "4 March 2024",
    "ai_work_images": [
      {"url": "https://www.thisiscolossal.com/wp-content/uploads/2024/02/gmunk-1.jpg", "caption": "Stable Diffusion-morphed volumetric cloud render from GMUNK's HP Z8 'CoCreated' pipeline behind Milky Chance's 'Synchronize' video (This Is Colossal, 2024)."},
      {"url": "https://www.thisiscolossal.com/wp-content/uploads/2024/02/gmunk-3.jpg", "caption": "AI-generated bioluminescent alien-flora landscape (Stable Diffusion still) from GMUNK's HP/Milky Chance AI project."}
    ]
  },
  {
    "name": "Chad Nelson", "domain": "Creative Direction / Film",
    "credentials": "Award-winning creative director with ~25 years of experience, now a Creative Specialist at OpenAI; directed the short film 'Critterz,' whose characters were designed with DALL-E and then animated.",
    "credentials_source": "https://www.c21media.net/department/marketing/content-london-exclusive-openais-chad-nelson-to-showcase-how-sora-will-supercharge-creativity-in-content-london-keynote/",
    "credentials_date": "18 October 2024",
    "quote": "I was truly floored. I wouldn't say it was the greatest monster design I've ever seen. But what it did do is it captured wonder.",
    "quote_source": "https://zackarnold.com/artificial-intelligence-future-of-creativity-chad-nelson/",
    "quote_date": "27 February 2024 (approx.)",
    "ai_work_images": [
      {"url": "https://images.squarespace-cdn.com/content/v1/642e34cfcfc3b2214f84cb2c/dfa821a1-c5de-4647-8e99-3b4d72e092fc/Screen+Shot+2023-04-05+at+8.08.30+PM.png", "caption": "Process shot: Chad Nelson in OpenAI's DALL-E editor generating a 'Critterz' character - from his DALL-E-designed short film."},
      {"url": "https://images.squarespace-cdn.com/content/v1/642e34cfcfc3b2214f84cb2c/4ec96b17-442e-4495-8ec3-41bbe0e58525/Screen+Shot+2023-04-05+at+8.06.57+PM.png", "caption": "A Critterz character in a forest - designed with OpenAI's DALL-E, then animated, from Nelson's short film."}
    ]
  },
  {
    "name": "Karen X. Cheng", "domain": "Creative Direction / Viral AI Campaigns",
    "credentials": "Director and creative known for viral generative-AI creative campaigns; advisor to Runway, collaborator with Adobe Firefly, and a featured creator in NVIDIA's 'In the NVIDIA Studio' series.",
    "credentials_source": "https://blogs.nvidia.com/blog/in-the-nvidia-studio-may-10/",
    "credentials_date": "10 May 2022",
    "quote": "I never had much drawing skill before, so I feel like I have art superpowers. Human plus AI is going to be better than AI alone for a very, very, very long time.",
    "quote_source": "https://blogs.nvidia.com/blog/in-the-nvidia-studio-may-10/",
    "quote_date": "10 May 2022",
    "ai_work_images": [
      {"url": "https://blogs.nvidia.com/wp-content/uploads/2022/05/karenxcheng-2-1-672x360.jpg", "caption": "NVIDIA Canvas (GauGAN2) before/after: Cheng's rough color-block doodle turned into a photorealistic mountain-lake landscape by the AI."},
      {"url": "https://blogs.nvidia.com/wp-content/uploads/2022/05/karenxcheng-4-1-672x378.jpg", "caption": "NVIDIA Canvas (GauGAN2) before/after: a scribbled sketch converted by the AI into a photorealistic sunset-over-ocean landscape."}
    ]
  },
  {
    "name": "Aurore Lechien", "domain": "Brand / Art Direction",
    "credentials": "Design Director at Base Design (Brussels), an internationally recognized branding studio; provided creative direction on the AI-assisted La Monnaie opera 2023-24 season campaign.",
    "credentials_source": "https://www.itsnicethat.com/news/base-design-la-monnaie-digital-180923",
    "credentials_date": "18 September 2023",
    "quote": "It was so fun. We just had fun for hours.",
    "quote_source": "https://www.itsnicethat.com/features/shades-of-intelligence-insights-research-creative-industry-ai-151123",
    "quote_date": "15 November 2023",
    "ai_work_images": [
      {"url": "https://basedesign2.imgix.net/images/baseweb_asset_lamonnaiefate_01.avif?auto=format,compress&fit=max&w=2020", "caption": "Grid of AI-generated opera-season posters from Base Design's La Monnaie 2023-24 'There will be Fate' campaign - visuals generated by feeding one-line play summaries as prompts into AI image tools."}
    ]
  },
  {
    "name": "Jessica Walsh", "domain": "Brand / Agency",
    "credentials": "Founder and creative director of the New York agency &Walsh (clients include Barneys, Snapchat, Levi's); previously partner at Sagmeister & Walsh; founder of the mentorship nonprofit Ladies, Wine & Design. Her studio rebranded nuclear-advocacy project Isodope using DALL-E.",
    "credentials_source": "https://en.wikipedia.org/wiki/Jessica_Walsh",
    "credentials_date": "n/a - living reference",
    "quote": "AI is already here, and it will continue to have an exponentially large presence in the creative world. We can choose to ignore it and become outdated by it. Or we can choose to find creative ways to work with it and push our work further into territories that we couldn't have before.",
    "quote_source": "https://www.creativeboom.com/inspiration/isodope-walsh/",
    "quote_date": "6 October 2022",
    "ai_work_images": [
      {"url": "https://www.creativeboom.com/upload/articles/bd/bddb0c88810775bf4c5b4fd5997df1f2b3072eeb_800.jpg", "caption": "Isodope - &Walsh's rebrand of nuclear energy, its imagery developed with DALL-E (Creative Boom)."},
      {"url": "https://www.creativeboom.com/upload/articles/00/002490ec10711678cbc95a26d85f89366fab177e_944.jpg", "caption": "Another AI-generated visual from the &Walsh x Isodope DALL-E campaign."}
    ]
  },
  {
    "name": "Pum Lefebure", "domain": "Creative Direction / Advertising",
    "credentials": "Co-founder and Chief Creative Officer of Washington, D.C. agency Design Army (clients include Adobe, Disney, Netflix, Bloomingdale's, PepsiCo); her studio produced the fully AI-generated 'Adventures in A-Eye' campaign for Georgetown Optician using Midjourney.",
    "credentials_source": "https://www.commarts.com/exhibit/georgetown-optician-a-eye-campaign",
    "credentials_date": "26 April 2023",
    "quote": "I love that this is a new beginning of creative possibilities! And I'm proud that - in working with AI - we never lost our sense of creativity and craft. We didn't let AI control us.",
    "quote_source": "https://invisionmag.com/georgetown-optician-embraces-ai-tech-with-adventures-in-a-eye-ad-campaign/",
    "quote_date": "March 2023",
    "ai_work_images": [
      {"url": "https://image.commarts.com/images1/1/2/5/1/1/1152168_102_600_OTEyMzY0MTU4LTk2NDg2MDY4Mw_f.jpg", "caption": "Design Army's fully AI-generated 'Adventures in A-Eye' campaign for Georgetown Optician, made with Midjourney (Communication Arts)."},
      {"url": "https://invisionmag.com/wp-content/uploads/2023/03/Georgetown-A-Eye-1.jpg", "caption": "Another 'Adventures in A-Eye' Midjourney-generated campaign visual by Design Army."}
    ]
  }
]

# Christoph Niemann added as #20 (group B hung; sourced his AI-feature image directly).
# Paula Scher left off: no verifiable direct AI-work image (Performance.gov icons not servable).
SCHER_NIEMANN = [
  {
    "name": "Christoph Niemann", "domain": "Editorial Illustration",
    "credentials": "Internationally renowned illustrator and graphic/editorial designer; creator of more than two dozen New Yorker covers, longtime New York Times Magazine contributor, and subject of an episode of Netflix's 'Abstract: The Art of Design'.",
    "credentials_source": "https://en.wikipedia.org/wiki/Christoph_Niemann",
    "credentials_date": "n/a - living reference",
    "quote": "When I first learned about computer tools in art school, I was elated. Despite my wariness of AI, I've found some good uses for it.",
    "quote_source": "https://kottke.org/25/06/how-christoph-niemann-uses-ai-in-his-work",
    "quote_date": "25 June 2025",
    "ai_work_images": [
      {"url": "https://kottke.org/plus/misc/images/niemann-ai.jpg", "caption": "Illustration from the feature 'How Christoph Niemann Uses AI in His Work' (kottke.org, June 2025), where Niemann details the AI tools he's folded into his illustration process."}
    ]
  }
]

def load_new():
    with open(os.path.join(ROOT, "new_artists.json"), encoding="utf-8") as f:
        return json.load(f)

def main():
    roster = list(KEEPERS) + list(SCHER_NIEMANN) + load_new()
    # normalize: ensure ai_work_images present
    for d in roster:
        d.setdefault("ai_work_images", [])
    print("TOTAL roster:", len(roster))
    for i, d in enumerate(roster, 1):
        print(f"{i:2d} {d['name']:<32} imgs:{len(d['ai_work_images'])}")
    with open(os.path.join(ROOT, "designers_v2.json"), "w", encoding="utf-8") as f:
        json.dump(roster, f, ensure_ascii=False, indent=2)
    print("wrote designers_v2.json")

if __name__ == "__main__":
    main()
