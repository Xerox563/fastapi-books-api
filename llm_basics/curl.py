# Simple get request
curl http://localhost:8000/health 
curl http://localhost:8000/health -o output.json # get the api and fetc an push the response int this output file .
# Fetch info, Health checks

# JSON post
curl -X POST http://localhost:8000/text \ 
      -H "Content-Type : application/json" \
      -D '{"prompt":"How are you !!"}'
# Sending JSON, AI prompts, Forms (non-file)

# File upload [Sending Binary File]
curl -X POST http://localhost:8000/image \ 
     -F "file=@photo.png"
# use when Upload images, Upload documents, Multipart data

# Pretty debug
curl -v http://localhost:8000/health

# Add auth Token
curl -H "Authorization: Bearer TOKEN" ...