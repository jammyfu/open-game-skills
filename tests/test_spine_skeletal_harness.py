"""Run the installable skill's executable fixtures in normal repository CI."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/2d/spine-skeletal/scripts'))
from test_audit_skin import AuditTests
from test_bind_joint import BindTests
from test_measure_surface import SurfaceTests

from test_attachment_ownership import OwnershipTests
