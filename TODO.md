# TODO - Cookiecutter Python Claude

## Completed ✅
- [x] Fix directory structure - remove duplicate project name
- [x] Fix conditional file generation for API endpoints  
- [x] Update hooks to handle directory creation properly
- [x] Test template generation to verify fixes

## Next Iteration 🚀

### High Priority
- [ ] Add Makefile with common development tasks
  - `make install` - setup development environment
  - `make test` - run tests with coverage
  - `make lint` - run all linting tools
  - `make format` - format code
  - `make docker-build` - build Docker images
  - `make docker-run` - run with Docker
  - `make clean` - cleanup generated files

- [ ] Configure comprehensive .gitignore file
  - Python-specific ignores (__pycache__, *.pyc, etc.)
  - FastAPI/web development ignores
  - Docker ignores
  - IDE ignores (VSCode, PyCharm, etc.)
  - OS ignores (macOS, Windows, Linux)
  - Environment and secrets

- [ ] Test project functionality after generation - verify /healthz endpoint works
  - Generate test project
  - Install dependencies  
  - Start FastAPI server
  - Test all health endpoints: /healthz, /livez, /readyz
  - Test items CRUD endpoints
  - Verify structured logging works

### Medium Priority  
- [ ] Create .claude/agents directory with specialized sub-agents
  - `fastapi-dev.md` - FastAPI development agent
  - `test-writer.md` - Test writing specialist
  - `docker-ops.md` - Docker operations agent
  - `api-designer.md` - API design specialist

### Future Enhancements
- [ ] Add more project types
  - `data-science` - with Jupyter, pandas, etc.
  - `ml-service` - with MLflow, model serving
  - `async-worker` - with Celery/RQ background tasks

- [ ] Enhanced testing setup
  - Integration test examples
  - Load testing with locust
  - API contract testing

- [ ] Monitoring and observability
  - Prometheus metrics
  - OpenTelemetry tracing
  - Health check dashboard

- [ ] Security enhancements
  - JWT authentication example
  - Rate limiting setup
  - Security headers middleware

## Notes
- All FastAPI projects now include Kubernetes-style health endpoints
- Template supports both CLI and web project types
- Docker support with multi-stage builds included
- Structured logging with correlation IDs implemented